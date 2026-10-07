# Document Intelligence & Question Extraction Service

A FastAPI-based service for extracting structured examination questions from PDFs and images without relying on external AI services at runtime. The system uses OCR and document-processing tools to parse input files, extract meaningful content, and structure the result into question-related data.

## Overview

This project is designed for document-heavy workflows where users upload PDFs or scanned images and need to extract question content in a structured format. It includes authentication, document ingestion, processing pipelines, and status tracking.

## Key Features

- FastAPI backend
- PDF and image upload support
- OCR-based extraction using Tesseract
- OpenCV and image preprocessing
- Redis-based asynchronous job processing
- Celery task queue support
- PostgreSQL persistence
- JWT-based authentication
- Document status tracking and result retrieval
- Question, answer, warning, and relation endpoints

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Redis
- Celery
- SQLAlchemy
- PyMuPDF
- Tesseract OCR
- OpenCV
- Pillow
- JWT authentication

## Run the Project

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Then open:

```text
http://localhost:8000/docs
```

## API Overview

### Authentication

- `/auth/register`
- `/auth/login`
- `/auth/me`

### Documents

- upload documents
- list documents
- view document details
- check processing status
- delete document

### Questions and Results

- question retrieval and linked answers
- warnings and relationships
- structured processing outputs

## Development Checks

```powershell
python -m pip install -r requirements.txt
pytest -q
python -m compileall -q app
```

## Environment Variables

This project expects configuration for:

- `DATABASE_URL`
- `REDIS_URL`
- `JWT_SECRET_KEY`
- `MAX_FILE_SIZE_MB`
- `UPLOAD_DIR`

## Notes

- Tesseract must be installed locally for OCR-based processing when running outside Docker.
- Docker handles the OCR environment automatically.
- The project is structured for extension and can be adapted to broader document-intelligence workflows.

## Portfolio Value

This project demonstrates:
- backend API design
- asynchronous processing with Celery and Redis
- OCR and document parsing workflows
- database-driven application architecture
- real-world data extraction automation
