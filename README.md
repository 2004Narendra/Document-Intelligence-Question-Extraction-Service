# Document Intelligence & Question Extraction Service

A FastAPI service for extracting structured examination questions from PDFs and images without external AI services. It uses PyMuPDF, Tesseract, OpenCV, Pillow, PostgreSQL, Redis, Celery, SQLAlchemy, Alembic, JWT, and Pytest.

## Run

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Open `http://localhost:8000/docs`.

Register and log in to receive a bearer token, then upload a PDF/JPG/JPEG/PNG to `POST /documents`. The response is immediate with `UPLOADED`; poll `GET /documents/{id}/status` until `COMPLETED` or `FAILED`.

## Development checks

```powershell
python -m pip install -r requirements.txt
pytest -q
python -m compileall -q app
```

Tesseract must be installed locally for OCR tests and image processing. Docker installs it automatically. Configure `DATABASE_URL`, `REDIS_URL`, `JWT_SECRET_KEY`, `MAX_FILE_SIZE_MB`, and `UPLOAD_DIR` in `.env`.

## API groups

Authentication: `/auth/register`, `/auth/login`, `/auth/me`

Documents: upload/list/detail/status/delete, questions, answers, warnings, and relations

Questions: `/questions/{question_id}`

The Postman collection is in `postman/document-intelligence.postman_collection.json`, and a parser fixture is in `samples/sample_questions.txt`.
