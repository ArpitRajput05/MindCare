"""
Unit Tests for RAG Engine & Knowledge Base
"""

import pytest
from app.services.rag_engine import rag_engine


def test_rag_engine_index_status():
    count = rag_engine.collection.count()
    assert count >= 25, f"Expected at least 25 indexed chunks, found {count}"


def test_rag_retrieval_sleep():
    results = rag_engine.retrieve("How can a student improve circadian rhythm and sleep?", top_k=3)
    assert len(results) > 0
    top = results[0]
    assert len(top.snippet) > 0
    assert len(top.source) > 0
    assert len(top.title) > 0


def test_rag_retrieval_stress():
    results = rag_engine.retrieve("sensory grounding for anxiety and panic", top_k=2)
    assert len(results) > 0
    assert any("NHS" in r.source or "Grounding" in r.title or "Stress" in r.category for r in results)
