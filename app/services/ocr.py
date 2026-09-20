from pathlib import Path
import cv2
import numpy as np
import pytesseract
from PIL import Image


def preprocess_image(image: Image.Image) -> Image.Image:
    array = cv2.cvtColor(np.array(image.convert("RGB")), cv2.COLOR_RGB2GRAY)
    denoised = cv2.fastNlMeansDenoising(array, None, 10, 7, 21)
    thresholded = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return Image.fromarray(thresholded)


def image_to_text(path: str | Path) -> tuple[str, float]:
    image = Image.open(path)
    processed = preprocess_image(image)
    data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
    text = pytesseract.image_to_string(processed)
    confidences = [float(value) for value in data["conf"] if float(value) >= 0]
    quality = (sum(confidences) / len(confidences) / 100) if confidences else 0.0
    return text, round(min(1.0, quality), 2)
