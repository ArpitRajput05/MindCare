"""
MindCare Pydantic Data Models & Request/Response Schemas
Strictly typed for input validation, SHAP explainability, RAG retrieval, and LLM chat.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


# -------------------------------------------------------------------------
# Core Student Input Schema
# -------------------------------------------------------------------------
class StudentData(BaseModel):
    age: int = Field(..., ge=10, le=100, description="Student's age in years")
    gender: Literal["Male", "Female"]
    country: str = Field(..., description="Country of residence or study")
    academic_level: Literal["Undergraduate", "Graduate", "High School"]
    most_used_platform: Literal[
        "Facebook", "LinkedIn", "Instagram", "Snapchat",
        "Twitter", "YouTube", "TikTok", "LINE",
        "KakaoTalk", "VKontakte", "WhatsApp", "WeChat"
    ]
    purpose_of_use: Literal["Networking", "Education", "Entertainment", "News"]
    avg_daily_usage_hours: float = Field(..., ge=0.0, le=24.0, description="Daily social media usage")
    daily_unlocks: int = Field(..., ge=0, le=1000, description="Daily phone unlocks count")
    study_hours: float = Field(..., ge=0.0, le=24.0, description="Daily academic study hours")
    physical_activity_hours: float = Field(..., ge=0.0, le=24.0, description="Daily physical activity/exercise")
    sleep_hours_per_night: float = Field(..., ge=0.0, le=24.0, description="Hours of sleep per night")
    stress_level: Literal["Low", "Medium", "High", "Very High"]


# -------------------------------------------------------------------------
# ML Prediction Schemas
# -------------------------------------------------------------------------
class PredictionResponse(BaseModel):
    predicted_mental_health_score: float
    band: str = "Balanced"
    summary: str = ""


# -------------------------------------------------------------------------
# Explainability (SHAP) Schemas
# -------------------------------------------------------------------------
class FeatureImpact(BaseModel):
    feature: str
    category: str
    label: str
    user_value: str
    impact: float
    direction: Literal["negative", "positive"]
    description: str


class ExplainResponse(BaseModel):
    predicted_score: float
    base_score: float
    risk_factors: list[FeatureImpact]
    protective_factors: list[FeatureImpact]
    search_queries: list[str]


# -------------------------------------------------------------------------
# RAG Retrieval Schemas
# -------------------------------------------------------------------------
class RetrievedSource(BaseModel):
    doc_id: str
    title: str
    source: str
    category: str
    snippet: str
    relevance_score: float = 0.0


# -------------------------------------------------------------------------
# Safety & Helpline Schemas
# -------------------------------------------------------------------------
class HelplineInfo(BaseModel):
    name: str
    number: str
    region: str
    description: str


class SafetyAlert(BaseModel):
    is_crisis: bool = True
    trigger_detected: str = ""
    message: str
    helplines: list[HelplineInfo]
    medical_disclaimer: str


# -------------------------------------------------------------------------
# LLM Plan Generation Schemas
# -------------------------------------------------------------------------
class PlanRequest(BaseModel):
    student_data: StudentData
    focus_area: Optional[str] = None


class PlanStep(BaseModel):
    step_number: int
    title: str
    action: str
    target_driver: str
    source: str


class PlanResponse(BaseModel):
    predicted_score: float
    headline: str
    steps: list[PlanStep]
    retrieved_sources: list[RetrievedSource]
    safety_disclaimer: str
    provider_used: str


# -------------------------------------------------------------------------
# Interactive Chatbot Schemas
# -------------------------------------------------------------------------
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    history: list[ChatMessage] = []
    student_context: Optional[StudentData] = None


class ChatResponse(BaseModel):
    reply: str
    sources: list[RetrievedSource] = []
    is_crisis: bool = False
    safety_alert: Optional[SafetyAlert] = None
    medical_disclaimer: str
    provider_used: str = "local"
