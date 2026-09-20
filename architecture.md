# Architecture

The API accepts an authenticated upload, writes the source under a UUID filename, creates a `documents` row, and enqueues `process_document` in Celery. Redis transports the task and PostgreSQL stores durable state.

The worker extracts native PDF text with PyMuPDF. When text is shorter than 50 characters, it renders PDF pages and applies OpenCV preprocessing plus Tesseract OCR. The parser identifies numbered question blocks, options, answer-key lines, question types, source pages, and confidence evidence. Low-confidence or incomplete results are persisted as warnings and `review_required` records.

All document and child-resource reads use the authenticated user's `user_id` ownership predicate. Files are deleted with their database record. Docker Compose provides the API, worker, PostgreSQL, and Redis services.
