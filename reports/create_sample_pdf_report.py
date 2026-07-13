from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

FEATURES = {
    "radius_mean": 14.1,
    "texture_mean": 19.2,
    "perimeter_mean": 91.9,
    "area_mean": 654.8,
    "smoothness_mean": 0.096,
    "compactness_mean": 0.104,
    "concavity_mean": 0.089,
    "concave_points_mean": 0.049,
    "symmetry_mean": 0.181,
    "fractal_dimension_mean": 0.063,
}


def create_sample_pdf() -> str:
    output = Path(__file__).resolve().parent / "sample_breast_cancer_report.pdf"
    pdf = canvas.Canvas(str(output), pagesize=A4)
    width, height = A4
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, height - 60, "Sample Breast Cancer Diagnostic Report")
    pdf.setFont("Helvetica", 11)
    y = height - 100
    for label, value in FEATURES.items():
        pdf.drawString(50, y, f"{label}: {value}")
        y -= 22
    pdf.save()
    return str(output)


if __name__ == "__main__":
    print(create_sample_pdf())

