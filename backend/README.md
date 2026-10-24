# Backend: face photo validation

`server.py` serves the web page and validates face photos before anything is saved:

- `POST /check`: checks one photo (one face, big enough, sharp, well lit). Saves nothing.
- `POST /enroll`: validates the three photos together with `face_recognition_lite`.
  Only if they pass, it uploads them to the Supabase `faces` bucket and inserts the
  three rows in `face_templates`. Otherwise it returns which poses to retake.

Requires Python 3.11.

## Setup (once)

```bash
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install ../face_recognition_lite-0.1.0-py3-none-any.whl supabase fastapi uvicorn python-multipart
face-lite download-models          # needs internet
```

## Run the demo

From the repository root:

```powershell
$env:SUPABASE_URL = "https://<project>.supabase.co"
$env:SUPABASE_SERVICE_ROLE_KEY = "<secret key>"
.\.venv\Scripts\python.exe backend\server.py
```

Open `http://localhost:8000` on the computer.

### From a phone

The phone camera needs HTTPS, so expose the server with a free tunnel (no account):

```powershell
winget install --id Cloudflare.cloudflared
cloudflared tunnel --url http://localhost:8000
```

Open the `https://….trycloudflare.com` URL it prints. The URL changes on every run.

The secret key bypasses row level security: keep it in the terminal only, never in
the web page or in Git.

## Manual enrollment

`enroll.py <person_id>` still enrolls photos already stored in Supabase Storage.
