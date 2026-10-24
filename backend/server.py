"""Demo server: serves the web page and validates face photos before saving them.

    SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... python backend/server.py

Never expose the service role key in the web page.
"""
import os
import uuid
from pathlib import Path

import uvicorn
from face_lite import FaceEngine
from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import FileResponse
from supabase import create_client

ROOT = Path(__file__).resolve().parent.parent
BUCKET = "faces"
POSES = ("front", "left", "right")  # same order FaceEngine.enroll expects
MAX_PHOTO_BYTES = 10_000_000

db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
engine = FaceEngine(ROOT / "artifacts" / "models")  # loaded once, reused by every request
app = FastAPI()


def current_person_id(authorization: str | None) -> str:
    """The person is the signed-in user; never trust an id sent by the page."""
    token = (authorization or "").removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Missing session")
    try:
        user = db.auth.get_user(token).user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session")
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid session")
    return user.id


def read_photo(upload: UploadFile) -> bytes:
    data = upload.file.read(MAX_PHOTO_BYTES + 1)
    if len(data) > MAX_PHOTO_BYTES:
        raise HTTPException(status_code=413, detail="Photo too large")
    return data


@app.get("/")
def page():
    return FileResponse(ROOT / "index.html")


@app.post("/check")
def check(image: UploadFile = File(...), authorization: str | None = Header(None)):
    """Quick per-photo feedback: one face, big enough, sharp, well lit. Saves nothing."""
    current_person_id(authorization)
    result = engine.extract(read_photo(image))
    return {"status": result["status"], "reason": result.get("reason")}


@app.post("/enroll")
def enroll(
    front: UploadFile = File(...),
    left: UploadFile = File(...),
    right: UploadFile = File(...),
    authorization: str | None = Header(None),
):
    """Validate the three photos together; only if they pass, save them and the embeddings."""
    person_id = current_person_id(authorization)
    photos = [read_photo(front), read_photo(left), read_photo(right)]

    result = engine.enroll(
        images=photos,
        person_id=person_id,
        template_ids=[str(uuid.uuid4()) for _ in POSES],
    )
    if result["status"] != "enrolled":
        return {"status": result["status"], "captures": result["captures"]}

    rows = result["templates"]
    new_ids = [row["template_id"] for row in rows]
    try:
        db.table("face_templates").insert(rows).execute()  # three rows in one statement
        for pose, data in zip(POSES, photos):
            db.storage.from_(BUCKET).upload(
                f"{person_id}/{pose}.jpg", data, {"content-type": "image/jpeg", "upsert": "true"}
            )
    except Exception:
        db.table("face_templates").delete().in_("template_id", new_ids).execute()
        raise HTTPException(status_code=500, detail="Could not save the photos")

    # Replace any previous templates of this person.
    db.table("face_templates").delete().eq("person_id", person_id).not_.in_("template_id", new_ids).execute()
    return {"status": "enrolled"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
