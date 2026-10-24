# Backend: face enrollment

Reads the three photos of a person from the Supabase `faces` bucket, runs the
`face_recognition_lite` model and stores the three embeddings in `face_templates`.

Requires Python 3.11.

```bash
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install ../face_recognition_lite-0.1.0-py3-none-any.whl supabase
face-lite download-models          # needs internet, run once

export SUPABASE_URL=https://<project>.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=<service role key>   # Windows: $env:NAME = "value"
python backend/enroll.py <person_id>
```

Run it from the repository root so `artifacts/models` resolves. The service role
key bypasses row level security: keep it out of the web page and out of Git.
