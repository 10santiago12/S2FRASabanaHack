"""Turn the three photos of a person in Storage into face_templates rows.

Usage:
    SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... python backend/enroll.py <person_id>

Never expose the service role key in the web page.
"""
import os
import sys
import uuid

from face_lite import FaceEngine
from supabase import create_client

BUCKET = "faces"
POSES = ("front", "left", "right")  # same order FaceEngine.enroll expects
MODELS_DIR = "artifacts/models"


def enroll(person_id: str) -> int:
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
    engine = FaceEngine(MODELS_DIR)

    images = [db.storage.from_(BUCKET).download(f"{person_id}/{pose}.jpg") for pose in POSES]
    result = engine.enroll(
        images=images,
        person_id=person_id,
        template_ids=[str(uuid.uuid4()) for _ in POSES],
    )

    if result["status"] != "enrolled":
        for capture in result["captures"]:
            print(f"{capture['position']}: {capture['status']} ({capture['reason']})")
        print(f"enrollment not saved: {result['status']}")
        return 1

    # Insert the three new rows in one statement, then drop any previous templates.
    rows = result["templates"]
    db.table("face_templates").insert(rows).execute()
    new_ids = [row["template_id"] for row in rows]
    db.table("face_templates").delete().eq("person_id", person_id).not_.in_("template_id", new_ids).execute()
    print(f"enrolled {person_id} with model {result['model_version']}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python backend/enroll.py <person_id>")
    sys.exit(enroll(sys.argv[1]))
