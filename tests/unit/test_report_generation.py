from pathlib import Path

from app.reports.pdf_report import generate_prediction_pdf


def test_generate_prediction_pdf(tmp_path):
    path = generate_prediction_pdf(
        {
            "patient_id": 1,
            "prediction_result": "Benign",
            "confidence_score": 0.96,
            "model_used": "random_forest",
            "doctor_recommendations": "Dr. Asha Menon",
        },
        output_dir=str(tmp_path),
    )
    assert Path(path).exists()
    assert Path(path).suffix == ".pdf"

