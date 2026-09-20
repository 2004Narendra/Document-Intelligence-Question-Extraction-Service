from app.services.confidence import review_required, score_question
from app.services.parser import parse_questions


def test_parses_mcq_and_answer_key():
    text = """1. Which color is primary?\nA. Red\nB. Green\nC. Black\n\nANSWER KEY\n1-A"""
    questions, warnings, answers = parse_questions(text)
    assert len(questions) == 1
    assert questions[0].number == "1"
    assert questions[0].options[0]["label"] == "A"
    assert answers == {"1": "A"}
    assert questions[0].answer == "A"


def test_low_confidence_requires_review():
    assert review_required(score_question(True, True, False, False, 0.2))
