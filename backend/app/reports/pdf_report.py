from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_prediction_pdf(payload: dict, output_dir: str = "reports/generated") -> str:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    filename = directory / f"prediction_report_{payload.get('patient_id', 'guest')}.pdf"
    pdf = canvas.Canvas(str(filename), pagesize=A4)
    width, height = A4
    pdf.setTitle("Breast Cancer Prediction Report")
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 60, "Breast Cancer Prediction Report")
    pdf.setFont("Helvetica", 11)
    y = height - 100
    for label, value in payload.items():
        pdf.drawString(50, y, f"{label.replace('_', ' ').title()}: {value}")
        y -= 22
    pdf.drawString(50, y - 20, "Note: This AI report supports clinical decision-making and is not a diagnosis.")
    pdf.save()
    return str(filename)

