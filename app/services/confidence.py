def score_question(has_number: bool, has_text: bool, has_options: bool, has_answer: bool, ocr_quality: float) -> float:
    score = (0.20 if has_number else 0) + (0.30 if has_text else 0) + (0.20 if has_options else 0) + (0.20 if has_answer else 0) + (0.10 * max(0.0, min(1.0, ocr_quality)))
    return round(score, 2)


def review_required(confidence: float) -> bool:
    return confidence < 0.80
