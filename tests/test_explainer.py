"""
Unit Tests for SHAP Explainability Service
"""

import pytest
from app.models.schemas import StudentData
from app.services.explainer import explainer_service


def test_shap_explainer_computes_factors():
    student = StudentData(
        age=21,
        gender="Female",
        country="USA",
        academic_level="Graduate",
        most_used_platform="TikTok",
        purpose_of_use="Entertainment",
        avg_daily_usage_hours=7.5,
        daily_unlocks=160,
        study_hours=1.5,
        physical_activity_hours=0.5,
        sleep_hours_per_night=4.5,
        stress_level="Very High"
    )

    exp = explainer_service.explain(student)

    assert isinstance(exp.predicted_score, float)
    assert 0.0 <= exp.predicted_score <= 10.0
    assert isinstance(exp.base_score, float)
    assert len(exp.risk_factors) > 0
    assert len(exp.search_queries) > 0

    # Sleep or screen time should be a negative impact driver
    risk_categories = [r.category for r in exp.risk_factors]
    assert "Sleep" in risk_categories or "Screen Time" in risk_categories
