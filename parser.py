import re
from dataclasses import dataclass
from app.services.confidence import review_required, score_question

QUESTION_RE = re.compile(r"(?m)^\s*(?:Q(?:uestion)?\s*)?(\d+)[.)]?\s+(.+?)(?=^\s*(?:Q(?:uestion)?\s*)?\d+[.)]?\s+|\Z)", re.I | re.S)
OPTION_RE = re.compile(r"(?m)^\s*(?:\(([A-D])\)|([A-D])[.)])\s*(.+)$", re.I)
ANSWER_RE = re.compile(r"(?im)^\s*(?:Q\s*)?(\d+)\s*[.)-]?\s*([A-D]|TRUE|FALSE)\s*$")


@dataclass
class ParsedQuestion:
    number: str
    text: str
    options: list[dict]
    answer: str | None
    question_type: str
    confidence: float
    review_required: bool
    source_pages: list[int]


def parse_questions(text: str, ocr_quality: float = 1.0) -> tuple[list[ParsedQuestion], list[dict], dict[str, str]]:
    answer_lines = dict(ANSWER_RE.findall(text))
    blocks = list(QUESTION_RE.finditer(text))
    questions: list[ParsedQuestion] = []
    warnings: list[dict] = []
    for match in blocks:
        number, block = match.group(1), match.group(2).strip()
        options = [{"label": (item.group(1) or item.group(2)).upper(), "text": item.group(3).strip()} for item in OPTION_RE.finditer(block)]
        question_text = OPTION_RE.sub("", block).strip()
        answer = answer_lines.get(number)
        question_type = "MCQ" if options else ("TRUE_FALSE" if re.search(r"true\s*/\s*false", question_text, re.I) else "SHORT_ANSWER")
        confidence = score_question(True, bool(question_text), bool(options), answer is not None, ocr_quality)
        if not options and question_type == "MCQ":
            warnings.append({"warning_type": "MISSING_OPTIONS", "message": f"Question {number} has no options", "confidence": confidence})
        if answer is None and "ANSWER" in text.upper():
            warnings.append({"warning_type": "ANSWER_NOT_FOUND", "message": f"No answer found for question {number}", "confidence": 0.5})
        questions.append(ParsedQuestion(number, question_text, options, answer, question_type, confidence, review_required(confidence), [1]))
    if len(text) < 50:
        warnings.append({"warning_type": "LOW_OCR_QUALITY", "message": "Very little source text was extracted", "confidence": ocr_quality})
    return questions, warnings, answer_lines
