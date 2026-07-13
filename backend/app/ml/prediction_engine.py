from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
import pypdf
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.core.config import settings
from app.schemas.prediction import CancerFeatures


FEATURE_NAME_MAP = {
    "mean_radius": "mean radius",
    "mean_texture": "mean texture",
    "mean_perimeter": "mean perimeter",
    "mean_area": "mean area",
    "mean_smoothness": "mean smoothness",
    "mean_compactness": "mean compactness",
    "mean_concavity": "mean concavity",
    "mean_concave_points": "mean concave points",
    "mean_symmetry": "mean symmetry",
    "mean_fractal_dimension": "mean fractal dimension",
    "radius_error": "radius error",
    "texture_error": "texture error",
    "perimeter_error": "perimeter error",
    "area_error": "area error",
    "smoothness_error": "smoothness error",
    "compactness_error": "compactness error",
    "concavity_error": "concavity error",
    "concave_points_error": "concave points error",
    "symmetry_error": "symmetry error",
    "fractal_dimension_error": "fractal dimension error",
    "worst_radius": "worst radius",
    "worst_texture": "worst texture",
    "worst_perimeter": "worst perimeter",
    "worst_area": "worst area",
    "worst_smoothness": "worst smoothness",
    "worst_compactness": "worst compactness",
    "worst_concavity": "worst concavity",
    "worst_concave_points": "worst concave points",
    "worst_symmetry": "worst symmetry",
    "worst_fractal_dimension": "worst fractal dimension",
}


class PredictionEngine:
    def __init__(self) -> None:
        self.models: dict[str, Any] = {}
        self.best_model_name = "random_forest"
        self.feature_names = list(FEATURE_NAME_MAP.values())
        self._load_or_train()

    def _load_or_train(self) -> None:
        artifact_dir = Path(__file__).resolve().parents[3] / "ml_models" / "artifacts"
        model_bundle = artifact_dir / "model_bundle.joblib"
        if model_bundle.exists():
            bundle = joblib.load(model_bundle)
            self.models = bundle["models"]
            self.best_model_name = bundle["best_model"]
            self.feature_names = bundle["feature_names"]
            return

        data = load_breast_cancer()
        x_train, _, y_train, _ = train_test_split(
            data.data, data.target, test_size=0.2, random_state=42, stratify=data.target
        )
        model = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
            ]
        )
        model.fit(x_train, y_train)
        self.models = {"random_forest": model}
        self.best_model_name = "random_forest"
        self.feature_names = list(data.feature_names)

    def _frame(self, features: CancerFeatures) -> pd.DataFrame:
        row = {FEATURE_NAME_MAP[key]: value for key, value in features.model_dump().items()}
        return pd.DataFrame([row], columns=self.feature_names)

    def predict(self, features: CancerFeatures, algorithm: str = "best") -> dict[str, Any]:
        selected = self.best_model_name if algorithm == "best" else algorithm
        if selected not in self.models:
            selected = self.best_model_name
        model = self.models[selected]
        frame = self._frame(features)
        probabilities = model.predict_proba(frame)[0]
        benign_probability = float(probabilities[1])
        malignant_probability = float(probabilities[0])
        result = "Benign" if benign_probability >= malignant_probability else "Malignant"
        confidence = max(benign_probability, malignant_probability)
        return {
            "selected_model": selected,
            "prediction_result": result,
            "probability": benign_probability if result == "Benign" else malignant_probability,
            "confidence_score": confidence,
            "feature_contributions": self.feature_contributions(frame),
        }

    def feature_contributions(self, frame: pd.DataFrame) -> list[dict[str, float | str]]:
        values = frame.iloc[0].to_numpy(dtype=float)
        centered = values - np.nanmean(values)
        order = np.argsort(np.abs(centered))[::-1][:10]
        return [
            {
                "feature": self.feature_names[index],
                "value": float(values[index]),
                "contribution": float(centered[index]),
            }
            for index in order
        ]


prediction_engine = PredictionEngine()

print(pypdf.__version__)