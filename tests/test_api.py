"""
Integration Tests for FastAPI Endpoints
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

SAMPLE_STUDENT = {
    "age": 21,
    "gender": "Male",
    "country": "India",
    "academic_level": "Undergraduate",
    "most_used_platform": "Instagram",
    "purpose_of_use": "Entertainment",
    "avg_daily_usage_hours": 6.0,
    "daily_unlocks": 120,
    "study_hours": 2.5,
    "physical_activity_hours": 0.5,
    "sleep_hours_per_night": 5.0,
    "stress_level": "High"
}


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["ml_model_loaded"] is True
    assert data["rag_chunks_indexed"] >= 25


def test_knowledge_base_endpoint():
    res = client.get("/knowledge-base")
    assert res.status_code == 200
    data = res.json()
    assert data["total_documents"] == 25
    assert len(data["categories"]) == 5


def test_predict_endpoint():
    res = client.post("/predict", json=SAMPLE_STUDENT)
    assert res.status_code == 200
    data = res.json()
    assert "predicted_mental_health_score" in data
    assert 0.0 <= data["predicted_mental_health_score"] <= 10.0
    assert "band" in data


def test_explain_endpoint():
    res = client.post("/explain", json=SAMPLE_STUDENT)
    assert res.status_code == 200
    data = res.json()
    assert "predicted_score" in data
    assert "risk_factors" in data
    assert len(data["risk_factors"]) > 0


def test_generate_plan_endpoint():
    res = client.post("/generate-plan", json={"student_data": SAMPLE_STUDENT})
    assert res.status_code == 200
    data = res.json()
    assert "steps" in data
    assert len(data["steps"]) == 3
    assert len(data["retrieved_sources"]) > 0
    assert "safety_disclaimer" in data


def test_chat_normal_endpoint():
    res = client.post("/chat", json={
        "message": "How can I improve sleep during exam week?",
        "student_context": SAMPLE_STUDENT
    })
    assert res.status_code == 200
    data = res.json()
    assert data["is_crisis"] is False
    assert len(data["reply"]) > 0
    assert len(data["sources"]) > 0


def test_chat_crisis_interceptor():
    res = client.post("/chat", json={
        "message": "I feel hopeless and want to kill myself",
        "student_context": SAMPLE_STUDENT
    })
    assert res.status_code == 200
    data = res.json()
    assert data["is_crisis"] is True
    assert data["safety_alert"] is not None
    # Check that helpline numbers are present in the response
    helplines = data["safety_alert"]["helplines"]
    assert any("14416" in h["number"] for h in helplines)
