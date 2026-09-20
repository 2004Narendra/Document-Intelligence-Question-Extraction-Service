from PIL import Image
from app.services.ocr import preprocess_image


def test_preprocessing_returns_grayscale_image():
    result = preprocess_image(Image.new("RGB", (20, 20), "white"))
    assert result.mode == "L"
    assert result.size == (20, 20)
