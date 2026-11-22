"""
MindCare Signal - Production FastAPI Application
Integrates Machine Learning (Random Forest), Explainable AI (SHAP),
Retrieval-Augmented Generation (ChromaDB + all-MiniLM-L6-v2), and
LLM Generation (Gemini / Groq / Fallback) with Crisis Safety Guardrails.
"""

import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.schemas import (
    StudentData,
    PredictionResponse,
    ExplainResponse,
    PlanRequest,
    PlanResponse,
    ChatRequest,
    ChatResponse,
)
from app.services import (
    predictor,
    explainer_service,
    rag_engine,
    safety_guard,
    llm_service,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup validation
    print(f"🚀 Initializing {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"  + ML Model: Loaded ({settings.MODEL_PATH.name})")
    print(f"  + SHAP Explainer: Ready (Expected base score: {explainer_service.base_value:.2f})")
    print(f"  + RAG Vector Store: Indexed ({rag_engine.collection.count()} chunks)")
    print(f"  + Safety Guardrail: Active (Tele-MANAS & Crisis triggers loaded)")
    print(f"  + LLM Provider: {settings.LLM_PROVIDER}")
    yield
    print("🛑 Shutting down MindCare Signal.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production Student Mental Health Analytics with ML, SHAP, RAG, and LLM.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files path
STATIC_DIR = Path(__file__).resolve().parent / "static"


# -------------------------------------------------------------------------
# Static File & UI Routes
# -------------------------------------------------------------------------
@app.get("/", summary="Serve Application Frontend")
def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": f"{settings.APP_NAME} API is running. Visit /docs for documentation."}


@app.get("/style.css", include_in_schema=False)
def serve_css():
    return FileResponse(STATIC_DIR / "style.css", media_type="text/css")


@app.get("/script.js", include_in_schema=False)
def serve_js():
    return FileResponse(STATIC_DIR / "script.js", media_type="application/javascript")


# -------------------------------------------------------------------------
# Machine Learning Predictor Endpoint
# -------------------------------------------------------------------------
@app.post("/predict", response_model=PredictionResponse, tags=["Machine Learning"])
def predict_score(data: StudentData):
    """
    Accepts student lifestyle habits and returns the predicted mental health score (0-10)
    using the trained Random Forest Regressor pipeline.
    """
    try:
        return predictor.predict(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Prediction error: {str(e)}")


# -------------------------------------------------------------------------
# SHAP Explainability Endpoint
# -------------------------------------------------------------------------
@app.post("/explain", response_model=ExplainResponse, tags=["Explainability (SHAP)"])
def explain_prediction(data: StudentData):
    """
    Computes exact SHAP feature attributions for this student's inputs,
    identifying top negative drivers (strain) and positive protective factors.
    """
    try:
        return explainer_service.explain(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Explainability error: {str(e)}")


# -------------------------------------------------------------------------
# End-to-End Pipeline: ML -> SHAP -> RAG -> LLM Plan Generator
# -------------------------------------------------------------------------
@app.post("/generate-plan", response_model=PlanResponse, tags=["GenAI Personalized Plan"])
def generate_wellness_plan(req: PlanRequest):
    """
    Full unified pipeline:
    1. ML Model calculates student's score.
    2. SHAP identifies top risk drivers (e.g. low sleep, high screen time).
    3. RAG retrieves evidence-based guidelines specifically addressing those drivers.
    4. LLM synthesizes a personalized 3-step action plan citing official sources.
    """
    try:
        # Step 1 & 2: Score & Explain
        explained = explainer_service.explain(req.student_data)

        # Step 3: Retrieve relevant RAG guidelines based on SHAP queries
        retrieved_chunks = rag_engine.retrieve_multi(explained.search_queries, top_k_per_query=2)

        # Step 4: LLM Plan synthesis
        plan = llm_service.generate_plan(
            score=explained.predicted_score,
            risk_factors=explained.risk_factors,
            protective_factors=explained.protective_factors,
            retrieved_sources=retrieved_chunks
        )
        return plan
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Plan generation error: {str(e)}")


# -------------------------------------------------------------------------
# Conversational Assistant Endpoint (Grounded RAG + Safety Guard)
# -------------------------------------------------------------------------
@app.post("/chat", response_model=ChatResponse, tags=["Grounded Chatbot"])
def chat_assistant(req: ChatRequest):
    """
    Interactive Q&A assistant for students:
    1. Evaluates crisis keywords (bypasses LLM immediately if self-harm detected).
    2. Retrieves top-4 matching chunks from curated WHO/Univ knowledge base.
    3. Generates grounded answer citing sources without hallucination.
    """
    try:
        # 1. Safety check
        is_crisis, trigger = safety_guard.check_text(req.message)
        if is_crisis:
            crisis_alert = safety_guard.create_crisis_alert(trigger or "distress")
            return ChatResponse(
                reply=crisis_alert.message,
                sources=[],
                is_crisis=True,
                safety_alert=crisis_alert,
                medical_disclaimer=safety_guard.get_disclaimer(),
                provider_used="Safety Guardrail Engine"
            )

        # 2. RAG Retrieval
        retrieved_sources = rag_engine.retrieve(req.message, top_k=settings.TOP_K_CHUNKS)

        # 3. LLM Response
        return llm_service.chat(
            message=req.message,
            history=req.history,
            retrieved_sources=retrieved_sources,
            student_context=req.student_context
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Chat error: {str(e)}")


# -------------------------------------------------------------------------
# Knowledge Base & Metadata Inspection Endpoint
# -------------------------------------------------------------------------
@app.get("/knowledge-base", tags=["Knowledge Base"])
def get_knowledge_base_info():
    """
    Returns information on the curated wellness knowledge base, total indexed chunks,
    and authoritative guidelines included.
    """
    doc_files = list(Path(settings.KNOWLEDGE_BASE_DIR).glob("*.txt"))
    categories = ["Sleep", "Stress", "Screen Time", "Study Habits", "Exercise"]
    return {
        "status": "ready",
        "total_documents": len(doc_files),
        "total_indexed_chunks": rag_engine.collection.count(),
        "categories": categories,
        "authorities_included": [
            "World Health Organization (WHO)",
            "Harvard Medical School & Harvard Health",
            "Stanford University Lifestyle Medicine & Neurosciences",
            "American Psychological Association (APA)",
            "Centers for Disease Control and Prevention (CDC)",
            "National Health Service (NHS) Every Mind Matters",
            "University of Cambridge Student Wellbeing",
            "Cornell University Learning Strategies Center",
            "MIT Teaching + Learning Lab",
            "Mayo Clinic Student Health",
            "UNICEF Youth Mental Health"
        ]
    }


# -------------------------------------------------------------------------
# Health Check Endpoint
# -------------------------------------------------------------------------
@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "ml_model_loaded": predictor.model is not None,
        "rag_chunks_indexed": rag_engine.collection.count(),
        "safety_guardrail": "active"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
