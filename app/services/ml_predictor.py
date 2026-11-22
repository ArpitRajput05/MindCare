"""
MindCare ML Predictor Service
Loads the trained Random Forest Regressor Pipeline and handles inference.
"""

import os
import joblib
import pandas as pd
from app.config import settings
from app.models.schemas import StudentData, PredictionResponse


class MLPredictor:
    def __init__(self, model_path: str | os.PathLike | None = None):
        self.model_path = str(model_path or settings.MODEL_PATH)
        self.model = None
        self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found at: {self.model_path}")
        self.model = joblib.load(self.model_path)

    def to_dataframe(self, data: StudentData) -> pd.DataFrame:
        country_group = data.country if data.country in settings.TOP_COUNTRIES else "Other"
        return pd.DataFrame([{
            "Age": data.age,
            "Gender": data.gender,
            "Country": data.country,
            "Academic_Level": data.academic_level,
            "Most_Used_Platform": data.most_used_platform,
            "Purpose_Of_Use": data.purpose_of_use,
            "Avg_Daily_Usage_Hours": data.avg_daily_usage_hours,
            "Daily_Unlocks": data.daily_unlocks,
            "Study_Hours": data.study_hours,
            "Physical_Activity_Hours": data.physical_activity_hours,
            "Sleep_Hours_Per_Night": data.sleep_hours_per_night,
            "Stress_Level": data.stress_level,
            "Grouped_country": country_group
        }])

    def predict(self, data: StudentData) -> PredictionResponse:
        input_df = self.to_dataframe(data)
        raw_pred = float(self.model.predict(input_df)[0])
        score = round(max(0.0, min(10.0, raw_pred)), 2)

        if score < 4.5:
            band = "Strained"
            summary = "Your rhythm shows elevated strain. Small micro-shifts in sleep and digital boundaries can make a meaningful difference."
        elif score < 7.0:
            band = "Balanced"
            summary = "Your daily habits reflect a stable baseline with key opportunities to optimize energy and focus."
        else:
            band = "Strong"
            summary = "Your habits reflect a resilient, highly protective daily foundation. Excellent lifestyle balance."

        return PredictionResponse(
            predicted_mental_health_score=score,
            band=band,
            summary=summary
        )


predictor = MLPredictor()
