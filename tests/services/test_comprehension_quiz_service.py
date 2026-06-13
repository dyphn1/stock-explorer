"""
Smoke tests for comprehension_quiz_service.py.

Tests: get_questions, check_answer, calculate_score.
Uses the real comprehension_quiz.yaml config (no API calls, pure data lookup).
"""
import pytest

from src.services.comprehension_quiz_service import (
    get_questions,
    check_answer,
    calculate_score,
)


# ── get_questions() ───────────────────────────────────────────

class TestGetQuestions:
    def test_returns_list(self):
        result = get_questions()
        assert isinstance(result, list)

    def test_not_empty(self):
        result = get_questions()
        assert len(result) > 0

    def test_question_has_required_keys(self):
        questions = get_questions()
        for q in questions:
            assert "id" in q
            assert "text" in q
            assert "correct_key" in q
            assert "options" in q

    def test_question_options_are_tuples(self):
        questions = get_questions()
        for q in questions:
            for opt in q["options"]:
                assert isinstance(opt, tuple), f"Option should be tuple, got {type(opt)}"

    def test_option_has_3_elements(self):
        questions = get_questions()
        for q in questions:
            for opt in q["options"]:
                assert len(opt) == 3, f"Option should have 3 elements (key, label, explanation), got {len(opt)}"

    def test_correct_key_matches_an_option(self):
        questions = get_questions()
        for q in questions:
            option_keys = [opt[0] for opt in q["options"]]
            assert q["correct_key"] in option_keys, (
                f"Question '{q['id']}': correct_key '{q['correct_key']}' not in option keys {option_keys}"
            )

    def test_question_ids_are_unique(self):
        questions = get_questions()
        ids = [q["id"] for q in questions]
        assert len(ids) == len(set(ids)), "Question IDs should be unique"


# ── check_answer() ───────────────────────────────────────────

class TestCheckAnswer:
    def test_correct_answer(self):
        questions = get_questions()
        if not questions:
            pytest.skip("No questions available")
        q = questions[0]
        result = check_answer(q["id"], q["correct_key"])
        assert result["correct"] is True
        assert result["correct_key"] == q["correct_key"]
        assert len(result["explanation"]) > 0

    def test_incorrect_answer(self):
        questions = get_questions()
        if not questions:
            pytest.skip("No questions available")
        q = questions[0]
        # Pick a wrong key (any option key that is not correct)
        wrong_keys = [opt[0] for opt in q["options"] if opt[0] != q["correct_key"]]
        if not wrong_keys:
            pytest.skip("No wrong options available")
        result = check_answer(q["id"], wrong_keys[0])
        assert result["correct"] is False
        assert result["correct_key"] == q["correct_key"]
        assert len(result["explanation"]) > 0

    def test_nonexistent_question(self):
        result = check_answer("nonexistent_id", "a")
        assert result["correct"] is False
        assert "找不到題目" in result["explanation"]
        assert result["correct_key"] == ""

    def test_return_keys(self):
        questions = get_questions()
        if not questions:
            pytest.skip("No questions available")
        result = check_answer(questions[0]["id"], "a")
        assert "correct" in result
        assert "explanation" in result
        assert "correct_key" in result


# ── calculate_score() ────────────────────────────────────────

class TestCalculateScore:
    def test_all_correct(self):
        questions = get_questions()
        if not questions:
            pytest.skip("No questions available")
        answers = {q["id"]: q["correct_key"] for q in questions}
        result = calculate_score(answers)
        assert result["correct_count"] == result["total"]
        assert result["percentage"] == 100.0
        assert len(result["results"]) == result["total"]

    def test_all_wrong(self):
        questions = get_questions()
        if not questions:
            pytest.skip("No questions available")
        answers = {}
        for q in questions:
            wrong_keys = [opt[0] for opt in q["options"] if opt[0] != q["correct_key"]]
            if wrong_keys:
                answers[q["id"]] = wrong_keys[0]
        if not answers:
            pytest.skip("No questions with wrong options available")
        result = calculate_score(answers)
        assert result["correct_count"] == 0
        assert result["percentage"] == 0.0

    def test_partial_score(self):
        questions = get_questions()
        if len(questions) < 2:
            pytest.skip("Need at least 2 questions for partial score test")
        answers = {}
        for i, q in enumerate(questions):
            if i == 0:
                answers[q["id"]] = q["correct_key"]  # correct
            else:
                wrong_keys = [opt[0] for opt in q["options"] if opt[0] != q["correct_key"]]
                if wrong_keys:
                    answers[q["id"]] = wrong_keys[0]  # wrong
        result = calculate_score(answers)
        assert result["correct_count"] >= 1
        assert 0 < result["percentage"] < 100

    def test_empty_answers(self):
        result = calculate_score({})
        assert result["correct_count"] == 0
        assert result["total"] > 0
        assert result["percentage"] == 0.0
        assert len(result["results"]) == 0

    def test_return_structure(self):
        questions = get_questions()
        if not questions:
            pytest.skip("No questions available")
        answers = {questions[0]["id"]: questions[0]["correct_key"]}
        result = calculate_score(answers)
        assert "correct_count" in result
        assert "total" in result
        assert "percentage" in result
        assert "results" in result

    def test_result_items_have_question_text(self):
        questions = get_questions()
        if not questions:
            pytest.skip("No questions available")
        answers = {questions[0]["id"]: questions[0]["correct_key"]}
        result = calculate_score(answers)
        for r in result["results"]:
            assert "question_id" in r
            assert "question_text" in r
            assert "correct" in r
            assert "explanation" in r
            assert "selected_key" in r
            assert "correct_key" in r

    def test_unknown_question_id_skipped(self):
        result = calculate_score({"nonexistent_id": "a"})
        assert result["correct_count"] == 0
        assert len(result["results"]) == 0
