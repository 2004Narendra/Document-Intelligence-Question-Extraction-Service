from pathlib import Path
import re
import fitz
from app.services.ocr import image_to_text


def normalize_text(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text.replace("\r", "")).strip()


def extract_document_text(path: str | Path, file_type: str) -> tuple[str, float, dict[str, list[int]]]:
    path = Path(path)
    if file_type == "application/pdf":
        pages: list[str] = []
        page_map: dict[str, list[int]] = {}
        with fitz.open(path) as pdf:
            for page_number, page in enumerate(pdf, 1):
                text = normalize_text(page.get_text())
                pages.append(text)
                page_map[str(page_number)] = [page_number]
            combined = "\n".join(pages)
            if len(combined) >= 50:
                return combined, 1.0, page_map
            ocr_pages = []
            qualities = []
            for page_number, page in enumerate(pdf, 1):
                pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                image_path = path.with_name(f".{path.stem}-{page_number}.png")
                pixmap.save(image_path)
                try:
                    page_text, quality = image_to_text(image_path)
                    ocr_pages.append(normalize_text(page_text))
                    qualities.append(quality)
                finally:
                    image_path.unlink(missing_ok=True)
            return "\n".join(ocr_pages), (sum(qualities) / len(qualities) if qualities else 0.0), page_map
    text, quality = image_to_text(path)
    return normalize_text(text), quality, {"1": [1]}
