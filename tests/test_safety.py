"""
Unit Tests for Safety & Crisis Guardrail System
"""

import pytest
from app.services.safety_guard import safety_guard


def test_safety_guard_detects_crisis():
    crisis_phrases = [
        "I feel like killing myself tonight",
        "I want to end my life, I cannot take the stress",
        "Thinking about suicide and overdosing",
        "I feel hopeless and want to self-harm"
    ]

    for phrase in crisis_phrases:
        is_crisis, trigger = safety_guard.check_text(phrase)
        assert is_crisis is True, f"Failed to detect crisis in: '{phrase}'"
        assert trigger is not None


def test_safety_guard_ignores_normal_queries():
    normal_phrases = [
        "How can I sleep better before my exam?",
        "Tips to reduce phone screen time while studying",
        "What are the benefits of walking after lunch?",
        "How does the Pomodoro technique work?"
    ]

    for phrase in normal_phrases:
        is_crisis, _ = safety_guard.check_text(phrase)
        assert is_crisis is False, f"False positive crisis on: '{phrase}'"


def test_safety_guard_helpline_payload():
    alert = safety_guard.create_crisis_alert("test trigger")
    assert alert.is_crisis is True
    assert len(alert.helplines) >= 4

    # Ensure Tele-MANAS (14416) is included for India
    tele_manas = next((h for h in alert.helplines if "14416" in h.number), None)
    assert tele_manas is not None
    assert "Tele-MANAS" in tele_manas.name
