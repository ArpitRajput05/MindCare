"""
Unit Tests for Machine Learning Predictor
"""

import pytest
from app.models.schemas import StudentData
from app.services.ml_predictor import predictor


def get_sample_student(sleep_hours=6.5, stress="Medium", screen_time=4.0):
    return StudentData(
        age=20,
        gender="Male",
        country="India",
        academic_level="Undergraduate",
        most_used_platform="Instagram",
        purpose_of_use="Entertainment",
        avg_daily_usage_hours=screen_time,
        daily_unlocks=80,
        study_hours=3.5,
        physical_activity_hours=1.5,
        sleep_hours_per_night=sleep_hours,
        stress_level=stress
    )


def test_predictor_basic_inference():
    student = get_sample_student()
    res = predictor.predict(student)

    assert isinstance(res.predicted_mental_health_score, float)
    assert 0.0 <= res.predicted_mental_health_score <= 10.0
    assert res.band in ["Strained", "Balanced", "Strong"]
    assert len(res.summary) > 0


def test_predictor_unseen_country_defaults_to_other():
    student = get_sample_student()
    student.country = "New Zealand"  # Not in top_countries list
    res = predictor.predict(student)

    assert 0.0 <= res.predicted_mental_health_score <= 10.0
