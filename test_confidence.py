from app.services.confidence import score_question


def test_full_question_score_is_high():
    assert score_question(True, True, True, True, 1.0) == 1.0


def test_missing_evidence_lowers_score():
    assert score_question(True, True, False, False, 0.0) == 0.5
