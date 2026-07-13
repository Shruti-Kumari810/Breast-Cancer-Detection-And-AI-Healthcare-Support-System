from backend.app.db.session import SessionLocal
from backend.app.models.doctor import Doctor
from backend.app.models.resource import HealthResource


DOCTORS = [
    ("Dr. Asha Menon", "Breast Surgical Oncologist", "City Cancer Institute", "Bengaluru", 18, "+91-90000-10001"),
    ("Dr. Priya Rao", "Medical Oncologist", "Hope Oncology Centre", "Mumbai", 14, "+91-90000-10002"),
    ("Dr. Neha Kapoor", "Radiation Oncologist", "Care Specialty Hospital", "Delhi", 12, "+91-90000-10003"),
    ("Dr. Meera Sharma", "Breast Imaging Specialist", "Sunrise Diagnostics", "Hyderabad", 10, "+91-90000-10004"),
]

RESOURCES = [
    ("Breast Cancer Awareness", "Learn risk factors, screening methods, and the value of early detection.", "awareness", "https://www.cancer.org/"),
    ("Early Symptoms", "Persistent lump, nipple discharge, skin dimpling, or unexplained breast pain should be reviewed by a clinician.", "symptoms", "https://www.cdc.gov/cancer/breast/"),
    ("Prevention Tips", "Maintain healthy weight, limit alcohol, stay active, and follow screening guidance.", "prevention", "https://www.who.int/"),
    ("Nutrition Guidance", "Choose fiber-rich foods, lean proteins, fruits, vegetables, and adequate hydration during care.", "nutrition", "https://www.cancer.gov/"),
    ("Mental Health Support", "Counseling, support groups, and patient navigators can reduce distress during diagnosis and treatment.", "mental_health", "https://www.cancer.net/"),
    ("Emergency Contacts", "Seek urgent care for severe pain, breathing difficulty, high fever, or sudden swelling.", "emergency", "tel:112"),
]


def seed() -> None:
    db = SessionLocal()
    try:
        if not db.query(Doctor).first():
            db.add_all(
                [
                    Doctor(
                        doctor_name=name,
                        specialization=specialization,
                        hospital_name=hospital,
                        city=city,
                        experience=experience,
                        contact=contact,
                    )
                    for name, specialization, hospital, city, experience, contact in DOCTORS
                ]
            )
        if not db.query(HealthResource).first():
            db.add_all(
                [
                    HealthResource(title=title, description=description, resource_type=kind, url=url)
                    for title, description, kind, url in RESOURCES
                ]
            )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()

