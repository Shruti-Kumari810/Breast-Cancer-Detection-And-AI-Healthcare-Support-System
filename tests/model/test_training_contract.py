import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from app.ml.prediction_engine import PredictionEngine  # noqa: E402
from app.schemas.prediction import CancerFeatures  # noqa: E402


def test_prediction_engine_contract():
    engine = PredictionEngine()
    result = engine.predict(CancerFeatures(mean_radius=14, mean_texture=19, mean_perimeter=92, mean_area=650, mean_smoothness=0.1))
    assert result["prediction_result"] in {"Benign", "Malignant"}
    assert 0 <= result["confidence_score"] <= 1
    assert result["feature_contributions"]

