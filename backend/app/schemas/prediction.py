from datetime import datetime

from pydantic import BaseModel, Field


class CancerFeatures(BaseModel):
    mean_radius: float
    mean_texture: float
    mean_perimeter: float
    mean_area: float
    mean_smoothness: float
    mean_compactness: float = 0.1
    mean_concavity: float = 0.08
    mean_concave_points: float = 0.04
    mean_symmetry: float = 0.18
    mean_fractal_dimension: float = 0.06
    radius_error: float = 0.4
    texture_error: float = 1.2
    perimeter_error: float = 2.8
    area_error: float = 40.0
    smoothness_error: float = 0.007
    compactness_error: float = 0.025
    concavity_error: float = 0.03
    concave_points_error: float = 0.012
    symmetry_error: float = 0.02
    fractal_dimension_error: float = 0.004
    worst_radius: float = 16.0
    worst_texture: float = 25.0
    worst_perimeter: float = 105.0
    worst_area: float = 880.0
    worst_smoothness: float = 0.13
    worst_compactness: float = 0.25
    worst_concavity: float = 0.27
    worst_concave_points: float = 0.11
    worst_symmetry: float = 0.29
    worst_fractal_dimension: float = 0.08


class PredictionRequest(BaseModel):
    patient_id: int | None = None
    algorithm: str = Field(default="best", pattern="^(best|logistic_regression|svm|random_forest)$")
    features: CancerFeatures


class PredictionResponse(BaseModel):
    prediction_id: int | None = None
    selected_model: str
    prediction_result: str
    probability: float
    confidence_score: float
    feature_contributions: list[dict[str, float | str]] = []


class PredictionOut(BaseModel):
    prediction_id: int
    patient_id: int
    algorithm_used: str
    prediction_result: str
    confidence_score: float
    prediction_date: datetime

    model_config = {"from_attributes": True}

