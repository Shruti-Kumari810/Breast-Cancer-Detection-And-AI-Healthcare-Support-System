import io
import re

import pandas as pd
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.ml.prediction_engine import FEATURE_NAME_MAP
from app.reports.pdf_report import generate_prediction_pdf
from app.schemas.prediction import CancerFeatures
from app.schemas.prediction import PredictionOut, PredictionRequest, PredictionResponse
from app.services.prediction_service import PredictionService

router = APIRouter(dependencies=[Depends(get_current_user)])

FEATURE_ALIASES = {
    "mean_radius": ["mean_radius", "mean radius", "radius_mean", "radius mean"],
    "mean_texture": ["mean_texture", "mean texture", "texture_mean", "texture mean"],
    "mean_perimeter": ["mean_perimeter", "mean perimeter", "perimeter_mean", "perimeter mean"],
    "mean_area": ["mean_area", "mean area", "area_mean", "area mean"],
    "mean_smoothness": ["mean_smoothness", "mean smoothness", "smoothness_mean", "smoothness mean"],
    "mean_compactness": ["mean_compactness", "mean compactness", "compactness_mean"],
    "mean_concavity": ["mean_concavity", "mean concavity", "concavity_mean"],
    "mean_concave_points": ["mean_concave_points", "mean concave points", "concave_points_mean", "concave points_mean"],
    "mean_symmetry": ["mean_symmetry", "mean symmetry", "symmetry_mean"],
    "mean_fractal_dimension": ["mean_fractal_dimension", "mean fractal dimension", "fractal_dimension_mean"],
    "radius_error": ["radius_error", "radius error", "radius_se", "radius se"],
    "texture_error": ["texture_error", "texture error", "texture_se", "texture se"],
    "perimeter_error": ["perimeter_error", "perimeter error", "perimeter_se", "perimeter se"],
    "area_error": ["area_error", "area error", "area_se", "area se"],
    "smoothness_error": ["smoothness_error", "smoothness error", "smoothness_se", "smoothness se"],
    "compactness_error": ["compactness_error", "compactness error", "compactness_se"],
    "concavity_error": ["concavity_error", "concavity error", "concavity_se"],
    "concave_points_error": ["concave_points_error", "concave points error", "concave_points_se"],
    "symmetry_error": ["symmetry_error", "symmetry error", "symmetry_se"],
    "fractal_dimension_error": ["fractal_dimension_error", "fractal dimension error", "fractal_dimension_se"],
    "worst_radius": ["worst_radius", "worst radius", "radius_worst", "radius worst"],
    "worst_texture": ["worst_texture", "worst texture", "texture_worst"],
    "worst_perimeter": ["worst_perimeter", "worst perimeter", "perimeter_worst"],
    "worst_area": ["worst_area", "worst area", "area_worst"],
    "worst_smoothness": ["worst_smoothness", "worst smoothness", "smoothness_worst"],
    "worst_compactness": ["worst_compactness", "worst compactness", "compactness_worst"],
    "worst_concavity": ["worst_concavity", "worst concavity", "concavity_worst"],
    "worst_concave_points": ["worst_concave_points", "worst concave points", "concave_points_worst"],
    "worst_symmetry": ["worst_symmetry", "worst symmetry", "symmetry_worst"],
    "worst_fractal_dimension": ["worst_fractal_dimension", "worst fractal dimension", "fractal_dimension_worst"],
}


@router.post("/predict", response_model=PredictionResponse)
def predict_cancer(payload: PredictionRequest, db: Session = Depends(get_db)):
    return PredictionService(db).predict(payload)


@router.post("/upload-report", response_model=PredictionResponse)
async def upload_report_for_prediction(
    file: UploadFile = File(...),
    algorithm: str = Form("best"),
    patient_id: int | None = Form(None),
    db: Session = Depends(get_db),
):
    content = await file.read()
    features = _extract_features_from_upload(file.filename or "", content)
    payload = PredictionRequest(patient_id=patient_id, algorithm=algorithm, features=features)
    return PredictionService(db).predict(payload)


@router.get("/history", response_model=list[PredictionOut])
def prediction_history(patient_id: int | None = None, db: Session = Depends(get_db)):
    return PredictionService(db).history(patient_id)


@router.post("/report")
def prediction_report(payload: dict):
    return {"report_path": generate_prediction_pdf(payload)}


def _extract_features_from_upload(filename: str, content: bytes) -> CancerFeatures:
    suffix = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if suffix == "csv":
        frame = pd.read_csv(io.BytesIO(content))
    elif suffix in {"txt", "tsv"}:
        text = content.decode("utf-8", errors="ignore")
        separator = "\t" if suffix == "tsv" else None
        frame = pd.read_csv(io.StringIO(text), sep=separator, engine="python")
    elif suffix == "pdf":
        return _extract_features_from_pdf(content)
    else:
        raise HTTPException(
            status_code=400,
            detail="Upload a CSV, TSV, TXT, or text-based PDF report containing the required numeric cancer features.",
        )

    if frame.empty:
        raise HTTPException(status_code=400, detail="The uploaded report does not contain any data rows.")

    row = frame.iloc[0].to_dict()
    normalized = {_normalize_key(key): value for key, value in row.items()}
    payload = {}
    for api_key, dataset_key in FEATURE_NAME_MAP.items():
        value = _find_feature_value(api_key, dataset_key, normalized)
        if value is not None and value != "":
            try:
                payload[api_key] = float(value)
            except (TypeError, ValueError) as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Feature '{api_key}' must be numeric, but received '{value}'.",
                ) from exc

    required = ["mean_radius", "mean_texture", "mean_perimeter", "mean_area", "mean_smoothness"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Report is missing required fields: {', '.join(missing)}",
        )
    return CancerFeatures(**payload)


def _extract_features_from_pdf(content: bytes) -> CancerFeatures:
    try:
        reader = PdfReader(io.BytesIO(content))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not read this PDF file.") from exc

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="This PDF does not contain selectable text. Please upload a text-based PDF or convert the report values into CSV.",
        )

    payload = {}
    for api_key, dataset_key in FEATURE_NAME_MAP.items():
        value = _find_feature_value_in_text(api_key, dataset_key, text)
        if value is not None:
            payload[api_key] = value

    required = ["mean_radius", "mean_texture", "mean_perimeter", "mean_area", "mean_smoothness"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=(
                "PDF text was read, but these required measurements were not found: "
                + ", ".join(missing)
                + ". Use labels like radius_mean: 14.1 or mean radius: 14.1."
            ),
        )
    return CancerFeatures(**payload)


def _normalize_key(value: str) -> str:
    return (
        str(value)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
        .replace("(", "")
        .replace(")", "")
    )


def _find_feature_value(api_key: str, dataset_key: str, normalized: dict) -> object | None:
    aliases = [api_key, dataset_key, *FEATURE_ALIASES.get(api_key, [])]
    for alias in aliases:
        value = normalized.get(_normalize_key(alias))
        if value is not None and value != "":
            return value
    return None


def _find_feature_value_in_text(api_key: str, dataset_key: str, text: str) -> float | None:
    aliases = [api_key, dataset_key, *FEATURE_ALIASES.get(api_key, [])]
    for alias in aliases:
        escaped = re.escape(alias).replace("\\ ", r"[\s_:-]+").replace("_", r"[\s_:-]+")
        pattern = rf"\b{escaped}\b\s*[:=\-]?\s*(-?\d+(?:\.\d+)?)"
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None
