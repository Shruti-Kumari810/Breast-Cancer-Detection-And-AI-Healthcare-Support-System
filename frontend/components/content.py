SUPPORT_CONTENT = [
    ("Breast Cancer Awareness", "Screening and early detection improve treatment options and outcomes."),
    ("Early Symptoms", "Watch for a new lump, nipple changes, skin dimpling, persistent pain, or unusual discharge."),
    ("Prevention Tips", "Stay active, maintain healthy weight, limit alcohol, avoid tobacco, and follow screening advice."),
    ("Nutrition Guidance", "Prioritize vegetables, fruits, whole grains, lean protein, hydration, and clinician-approved supplements."),
    ("Mental Health Support", "Counseling, peer support, family conversations, and patient navigators can reduce emotional burden."),
    ("Emergency Contacts", "Call local emergency services for breathing difficulty, severe pain, high fever, or sudden swelling."),
]

SUPPORT_ARTICLES = {
    "Breast Cancer Awareness": {
        "summary": "Understand risk, screening, and why early care matters.",
        "sections": [
            (
                "Why awareness matters",
                "Breast cancer can often be treated more effectively when changes are found early. Awareness helps patients notice body changes, attend screening, and seek specialist advice without delay.",
            ),
            (
                "Who should be alert",
                "Anyone can develop breast cancer, but risk can increase with age, family history, inherited gene changes, previous breast conditions, obesity, alcohol use, and some hormonal factors.",
            ),
            (
                "What to do next",
                "Learn your normal breast appearance, follow screening guidance from your clinician, and do not ignore a new lump, nipple change, skin dimpling, or persistent pain.",
            ),
        ],
    },
    "Early Symptoms": {
        "summary": "Know the warning signs that should be discussed with a clinician.",
        "sections": [
            (
                "Common warning signs",
                "A new lump, thickened breast tissue, nipple discharge, nipple inversion, breast swelling, redness, skin dimpling, or a persistent localized pain should be evaluated.",
            ),
            (
                "Symptoms are not always cancer",
                "Many breast changes are benign, including cysts and infections. Still, a doctor should review unexplained or persistent symptoms so the cause is clear.",
            ),
            (
                "Urgent review",
                "Seek urgent care for severe pain, fever, rapid swelling, breathing difficulty, or symptoms that worsen quickly.",
            ),
        ],
    },
    "Prevention Tips": {
        "summary": "Practical lifestyle habits that can support breast health.",
        "sections": [
            (
                "Healthy daily choices",
                "Regular physical activity, balanced nutrition, maintaining a healthy weight, limiting alcohol, and avoiding tobacco can reduce overall health risks.",
            ),
            (
                "Screening and follow-up",
                "Prevention also means early detection. Keep screening appointments and follow your clinician's plan if you have dense breasts, family history, or previous abnormal results.",
            ),
            (
                "Know your risk",
                "If close relatives had breast or ovarian cancer, ask a clinician whether risk assessment or genetic counseling is appropriate.",
            ),
        ],
    },
    "Nutrition Guidance": {
        "summary": "Food and hydration guidance during prevention, testing, or treatment.",
        "sections": [
            (
                "Balanced plate",
                "Prioritize vegetables, fruits, whole grains, lentils, beans, nuts, seeds, and lean protein. These foods support energy, digestion, and recovery.",
            ),
            (
                "During treatment",
                "Small frequent meals, hydration, and clinician-approved supplements may help when appetite is low. Report nausea, weight loss, or swallowing difficulty to your care team.",
            ),
            (
                "What to limit",
                "Limit alcohol and heavily processed foods. Avoid starting supplements during treatment without asking your oncologist because some may interact with therapy.",
            ),
        ],
    },
    "Mental Health Support": {
        "summary": "Emotional support for patients and families.",
        "sections": [
            (
                "It is normal to feel overwhelmed",
                "Fear, uncertainty, anger, sadness, and fatigue are common during testing or treatment. Emotional support is part of healthcare, not a luxury.",
            ),
            (
                "Helpful support options",
                "Counseling, patient navigators, peer groups, family meetings, journaling, breathing exercises, and spiritual care can reduce distress.",
            ),
            (
                "When to ask for help",
                "Ask for professional help if anxiety, low mood, sleep problems, or hopelessness persist or interfere with daily life.",
            ),
        ],
    },
    "Emergency Contacts": {
        "summary": "When to seek urgent help.",
        "sections": [
            (
                "Emergency symptoms",
                "Call local emergency services for breathing difficulty, chest pain, fainting, uncontrolled bleeding, confusion, high fever, or sudden severe swelling.",
            ),
            (
                "Treatment-related red flags",
                "Patients receiving cancer treatment should report fever, infection signs, severe vomiting, dehydration, or unusual bruising promptly.",
            ),
            (
                "Prepare contacts",
                "Keep your oncologist, nearest hospital, emergency number, and a trusted family contact saved on your phone.",
            ),
        ],
    },
}

CHATBOT_KNOWLEDGE = {
    "symptom": "Common symptoms include a new lump, nipple changes, skin dimpling, redness, swelling, discharge, or persistent pain. Please consult a clinician for any new or worrying change.",
    "report": "You can upload a CSV, TSV, or TXT report in the Patient Portal. At minimum it should include mean_radius, mean_texture, mean_perimeter, mean_area, and mean_smoothness.",
    "doctor": "Use Doctors Directory or Consult Doctor in the Patient Portal. You can filter by city and specialization, then book an appointment.",
    "appointment": "Open Patient Portal, go to Consult Doctor, choose a doctor ID, date, and time, then submit Book Appointment.",
    "malignant": "A malignant AI output means the pattern looks concerning. It is not a final diagnosis. Please consult an oncologist promptly.",
    "benign": "A benign AI output means the model found a lower-risk pattern, but ongoing symptoms or clinical concerns should still be reviewed by a doctor.",
    "diet": "A balanced diet with vegetables, fruits, whole grains, lean proteins, and hydration can support recovery. Ask your doctor before taking supplements.",
    "mental": "Feeling anxious is understandable. Consider speaking with a counselor, patient support group, trusted family member, or your care team.",
}

FEATURE_DEFAULTS = {
    "mean_radius": 14.1,
    "mean_texture": 19.2,
    "mean_perimeter": 91.9,
    "mean_area": 654.8,
    "mean_smoothness": 0.096,
    "mean_compactness": 0.104,
    "mean_concavity": 0.089,
    "mean_concave_points": 0.049,
    "mean_symmetry": 0.181,
    "mean_fractal_dimension": 0.063,
    "radius_error": 0.405,
    "texture_error": 1.217,
    "perimeter_error": 2.866,
    "area_error": 40.3,
    "smoothness_error": 0.007,
    "compactness_error": 0.025,
    "concavity_error": 0.032,
    "concave_points_error": 0.012,
    "symmetry_error": 0.021,
    "fractal_dimension_error": 0.004,
    "worst_radius": 16.27,
    "worst_texture": 25.7,
    "worst_perimeter": 107.3,
    "worst_area": 880.6,
    "worst_smoothness": 0.132,
    "worst_compactness": 0.254,
    "worst_concavity": 0.272,
    "worst_concave_points": 0.115,
    "worst_symmetry": 0.29,
    "worst_fractal_dimension": 0.084,
}
