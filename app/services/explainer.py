"""
MindCare SHAP Explainability Engine
Decomposes student mental health score predictions into actionable risk & protective drivers.
"""

from typing import Tuple, List
import numpy as np
import shap
from app.services.ml_predictor import predictor
from app.models.schemas import StudentData, FeatureImpact, ExplainResponse


class SHAPExplainer:
    def __init__(self):
        self.rf_model = predictor.model.named_steps["random forest"]
        self.preprocessor = predictor.model.named_steps["preprocessor"]
        self.explainer = shap.TreeExplainer(self.rf_model)
        self.base_value = float(self.explainer.expected_value[0] if isinstance(self.explainer.expected_value, (list, np.ndarray)) else self.explainer.expected_value)

    def explain(self, data: StudentData) -> ExplainResponse:
        input_df = predictor.to_dataframe(data)
        x_transformed = self.preprocessor.transform(input_df)
        shap_values = self.explainer(x_transformed).values[0]

        predicted_score = float(self.rf_model.predict(x_transformed)[0])
        clamped_score = round(max(0.0, min(10.0, predicted_score)), 2)

        # Map 38 transformed features back into structured domain factors
        # 0: Study_Hours
        # 1: Age
        # 2: Avg_Daily_Usage_Hours
        # 3: Daily_Unlocks
        # 4: Physical_Activity_Hours
        # 5: Sleep_Hours_Per_Night
        # 6: Stress_Level
        # 7..37: One-hot encoded categorical variables

        factors: List[FeatureImpact] = []

        # 1. Sleep Hours
        sleep_impact = float(shap_values[5])
        factors.append(FeatureImpact(
            feature="Sleep_Hours_Per_Night",
            category="Sleep",
            label="Nightly Sleep Duration",
            user_value=f"{data.sleep_hours_per_night} hrs/night",
            impact=round(sleep_impact, 2),
            direction="negative" if sleep_impact < 0 else "positive",
            description=(
                f"Sleep duration of {data.sleep_hours_per_night}h/night is below the 7-9h biological target, elevating cognitive fatigue."
                if data.sleep_hours_per_night < 7.0
                else f"Healthy sleep duration of {data.sleep_hours_per_night}h/night supports memory consolidation and emotional recovery."
            )
        ))

        # 2. Daily Screen Time
        screen_impact = float(shap_values[2])
        factors.append(FeatureImpact(
            feature="Avg_Daily_Usage_Hours",
            category="Screen Time",
            label="Daily Social Screen Time",
            user_value=f"{data.avg_daily_usage_hours} hrs/day",
            impact=round(screen_impact, 2),
            direction="negative" if screen_impact < 0 else "positive",
            description=(
                f"{data.avg_daily_usage_hours}h/day on {data.most_used_platform} consumes cognitive bandwidth and heightens digital fatigue."
                if data.avg_daily_usage_hours > 4.0
                else f"Controlled daily screen time ({data.avg_daily_usage_hours}h/day) keeps digital distraction manageable."
            )
        ))

        # 3. Perceived Stress Level
        stress_impact = float(shap_values[6])
        factors.append(FeatureImpact(
            feature="Stress_Level",
            category="Stress",
            label="Perceived Academic Stress",
            user_value=data.stress_level,
            impact=round(stress_impact, 2),
            direction="negative" if stress_impact < 0 else "positive",
            description=(
                f"Perceived stress is currently rated '{data.stress_level}', depleting daily resilience."
                if data.stress_level in ["High", "Very High"]
                else f"Low to moderate perceived stress helps maintain cognitive clarity."
            )
        ))

        # 4. Daily Phone Unlocks
        unlock_impact = float(shap_values[3])
        factors.append(FeatureImpact(
            feature="Daily_Unlocks",
            category="Screen Time",
            label="Daily Phone Unlocks",
            user_value=f"{data.daily_unlocks} unlocks",
            impact=round(unlock_impact, 2),
            direction="negative" if unlock_impact < 0 else "positive",
            description=(
                f"Frequent phone unlocks ({data.daily_unlocks}/day) fragment deep study focus and increase dopamine seeking."
                if data.daily_unlocks > 80
                else f"Moderate daily unlocks ({data.daily_unlocks}/day) reflects low device dependency."
            )
        ))

        # 5. Physical Activity
        activity_impact = float(shap_values[4])
        factors.append(FeatureImpact(
            feature="Physical_Activity_Hours",
            category="Exercise",
            label="Daily Physical Activity",
            user_value=f"{data.physical_activity_hours} hrs/day",
            impact=round(activity_impact, 2),
            direction="negative" if activity_impact < 0 else "positive",
            description=(
                f"Sedentary routine ({data.physical_activity_hours}h/day) limits endorphin release and stress buffer capacity."
                if data.physical_activity_hours < 1.0
                else f"Active lifestyle ({data.physical_activity_hours}h/day) provides significant mood and neuroprotective benefits."
            )
        ))

        # 6. Study Hours
        study_impact = float(shap_values[0])
        factors.append(FeatureImpact(
            feature="Study_Hours",
            category="Study Habits",
            label="Daily Study Routine",
            user_value=f"{data.study_hours} hrs/day",
            impact=round(study_impact, 2),
            direction="negative" if study_impact < 0 else "positive",
            description=(
                f"Study volume ({data.study_hours}h/day) without structured breaks risks cognitive overload."
                if data.study_hours > 6.0 or (data.study_hours < 1.5 and data.academic_level != "High School")
                else f"Balanced study routine of {data.study_hours}h/day supports steady academic pacing."
            )
        ))

        # Sort into risk factors (negative impact) and protective factors (positive impact)
        risk_factors = sorted([f for f in factors if f.impact < 0], key=lambda x: x.impact)
        protective_factors = sorted([f for f in factors if f.impact >= 0], key=lambda x: x.impact, reverse=True)

        # Generate targeted RAG search queries based on top negative drivers
        queries: List[str] = []
        for risk in risk_factors[:3]:
            if risk.category == "Sleep":
                queries.append("WHO sleep hygiene circadian rhythm young adults")
            elif risk.category == "Screen Time":
                queries.append("Stanford digital detox reducing screen time notifications")
            elif risk.category == "Stress":
                queries.append("NHS anxiety grounding stress management techniques")
            elif risk.category == "Exercise":
                queries.append("CDC aerobic physical activity mental health mood boost")
            elif risk.category == "Study Habits":
                queries.append("Cornell Pomodoro cognitive load study focus")

        if not queries:
            queries.append("WHO university student mental wellbeing resilience guidelines")

        return ExplainResponse(
            predicted_score=clamped_score,
            base_score=round(self.base_value, 2),
            risk_factors=risk_factors,
            protective_factors=protective_factors,
            search_queries=queries
        )


explainer_service = SHAPExplainer()
