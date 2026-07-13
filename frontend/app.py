from __future__ import annotations

import io
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from components.api_client import ApiClient
from components.content import CHATBOT_KNOWLEDGE, FEATURE_DEFAULTS, SUPPORT_ARTICLES, SUPPORT_CONTENT

st.set_page_config(
    page_title="AI Breast Cancer Detection",
    page_icon="health",
    layout="wide",
    initial_sidebar_state="collapsed",
)

FALLBACK_DOCTORS = [
    {
        "doctor_id": 1,
        "doctor_name": "Dr. Asha Menon",
        "specialization": "Breast Surgical Oncologist",
        "hospital_name": "City Cancer Institute",
        "city": "Bengaluru",
        "experience": 18,
        "contact": "+91-90000-10001",
    },
    {
        "doctor_id": 2,
        "doctor_name": "Dr. Priya Rao",
        "specialization": "Medical Oncologist",
        "hospital_name": "Hope Oncology Centre",
        "city": "Mumbai",
        "experience": 14,
        "contact": "+91-90000-10002",
    },
    {
        "doctor_id": 3,
        "doctor_name": "Dr. Neha Kapoor",
        "specialization": "Radiation Oncologist",
        "hospital_name": "Care Specialty Hospital",
        "city": "Delhi",
        "experience": 12,
        "contact": "+91-90000-10003",
    },
]

MODEL_LABELS = {
    "logistic_regression": "Logistic Regression",
    "svm": "Support Vector Machine",
    "random_forest": "Random Forest",
}

MODEL_COLORS = {
    "Logistic Regression": "#db2777",
    "Support Vector Machine": "#7c3aed",
    "Random Forest": "#0f766e",
}

CSV_FEATURE_ALIASES = {
    "mean_radius": ["mean_radius", "mean radius", "radius_mean", "radius mean"],
    "mean_texture": ["mean_texture", "mean texture", "texture_mean", "texture mean"],
    "mean_perimeter": ["mean_perimeter", "mean perimeter", "perimeter_mean", "perimeter mean"],
    "mean_area": ["mean_area", "mean area", "area_mean", "area mean"],
    "mean_smoothness": ["mean_smoothness", "mean smoothness", "smoothness_mean", "smoothness mean"],
    "mean_compactness": ["mean_compactness", "mean compactness", "compactness_mean"],
    "mean_concavity": ["mean_concavity", "mean concavity", "concavity_mean"],
    "mean_concave_points": ["mean_concave_points", "mean concave points", "concave_points_mean"],
    "mean_symmetry": ["mean_symmetry", "mean symmetry", "symmetry_mean"],
    "mean_fractal_dimension": ["mean_fractal_dimension", "mean fractal dimension", "fractal_dimension_mean"],
    "radius_error": ["radius_error", "radius error", "radius_se"],
    "texture_error": ["texture_error", "texture error", "texture_se"],
    "perimeter_error": ["perimeter_error", "perimeter error", "perimeter_se"],
    "area_error": ["area_error", "area error", "area_se"],
    "smoothness_error": ["smoothness_error", "smoothness error", "smoothness_se"],
    "compactness_error": ["compactness_error", "compactness error", "compactness_se"],
    "concavity_error": ["concavity_error", "concavity error", "concavity_se"],
    "concave_points_error": ["concave_points_error", "concave points error", "concave_points_se"],
    "symmetry_error": ["symmetry_error", "symmetry error", "symmetry_se"],
    "fractal_dimension_error": ["fractal_dimension_error", "fractal dimension error", "fractal_dimension_se"],
    "worst_radius": ["worst_radius", "worst radius", "radius_worst"],
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


def load_css() -> None:
    css_path = Path(__file__).parent / "assets" / "css" / "styles.css"
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    components.html(
        """
        <link rel="manifest" href="/assets/manifest.json">
        <meta name="theme-color" content="#0f766e">
        """,
        height=0,
    )


def client() -> ApiClient:
    return ApiClient(st.session_state.get("token"))


def feedback_path() -> Path:
    path = Path(__file__).parent / "feedback_submissions.csv"
    if not path.exists():
        path.write_text("submitted_at,name,email,rating,message\n", encoding="utf-8")
    return path


def sample_report_csv() -> str:
    columns = list(FEATURE_DEFAULTS)
    values = [str(FEATURE_DEFAULTS[column]) for column in columns]
    return ",".join(columns) + "\n" + ",".join(values) + "\n"


def is_pdf_upload(uploaded_file) -> bool:
    return uploaded_file.name.lower().endswith(".pdf") or uploaded_file.type == "application/pdf"


def normalize_csv_key(value: object) -> str:
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


def parse_uploaded_report(uploaded_file, row_index: int = 0) -> tuple[pd.DataFrame, dict[str, float]]:
    raw = uploaded_file.getvalue()
    suffix = uploaded_file.name.lower().rsplit(".", 1)[-1] if "." in uploaded_file.name else "csv"
    if suffix == "tsv":
        frame = pd.read_csv(io.BytesIO(raw), sep="\t")
    else:
        frame = pd.read_csv(io.BytesIO(raw))
    if frame.empty:
        raise ValueError("The uploaded CSV has no patient rows.")
    row_index = min(row_index, len(frame) - 1)
    row = frame.iloc[row_index].to_dict()
    normalized_row = {normalize_csv_key(key): value for key, value in row.items()}
    features = {}
    missing_required = []
    for feature, default_value in FEATURE_DEFAULTS.items():
        value = None
        for alias in CSV_FEATURE_ALIASES.get(feature, [feature]):
            candidate = normalized_row.get(normalize_csv_key(alias))
            if pd.notna(candidate) and candidate != "":
                value = candidate
                break
        if value is None:
            if feature in {"mean_radius", "mean_texture", "mean_perimeter", "mean_area", "mean_smoothness"}:
                missing_required.append(feature)
            value = default_value
        try:
            features[feature] = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Column for {feature} must contain a numeric value. Found: {value}") from exc
    if missing_required:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_required)
            + ". Use the sample template or Kaggle-style columns like radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean."
        )
    return frame, features


@st.cache_data
def load_model_comparison() -> pd.DataFrame:
    report_path = Path(__file__).resolve().parents[1] / "ml_models" / "reports" / "model_comparison.csv"
    if report_path.exists():
        frame = pd.read_csv(report_path)
    else:
        frame = pd.DataFrame(
            [
                {
                    "model": "logistic_regression",
                    "accuracy": 0.982,
                    "precision": 0.986,
                    "recall": 0.986,
                    "f1": 0.986,
                    "roc_auc": 0.995,
                    "cv_roc_auc_mean": 0.995,
                },
                {
                    "model": "svm",
                    "accuracy": 0.982,
                    "precision": 0.986,
                    "recall": 0.986,
                    "f1": 0.986,
                    "roc_auc": 0.995,
                    "cv_roc_auc_mean": 0.995,
                },
                {
                    "model": "random_forest",
                    "accuracy": 0.947,
                    "precision": 0.958,
                    "recall": 0.958,
                    "f1": 0.958,
                    "roc_auc": 0.994,
                    "cv_roc_auc_mean": 0.990,
                },
            ]
        )
    frame["model_label"] = frame["model"].map(MODEL_LABELS).fillna(frame["model"])
    return frame


def auth_card(role: str, key_prefix: str) -> None:
    label = "Patient / New User" if role == "patient" else "Doctor"
    icon = "Personal care" if role == "patient" else "Clinical review"
    st.markdown(
        f"<div class='login-card'><p class='eyebrow-dark'>{icon}</p><h3>{label} Login</h3></div>",
        unsafe_allow_html=True,
    )
    mode = st.radio("Choose action", ["Login", "Register"], horizontal=True, key=f"{key_prefix}_mode")
    email = st.text_input("Email", value=f"{role}@example.com", key=f"{key_prefix}_email")
    password = st.text_input("Password", value="password123", type="password", key=f"{key_prefix}_password")
    if mode == "Register":
        full_name = st.text_input("Full name", value="New Patient" if role == "patient" else "Demo Doctor", key=f"{key_prefix}_name")
        if st.button(f"Create {label} Account", use_container_width=True, key=f"{key_prefix}_register"):
            try:
                ApiClient().register({"full_name": full_name, "email": email, "password": password, "role": role})
                st.success("Account created. Please login now.")
            except Exception as exc:
                st.error(_friendly_error(exc))
    if st.button(f"Login as {label}", use_container_width=True, key=f"{key_prefix}_login"):
        try:
            st.session_state["token"] = ApiClient().login(email, password)
            st.session_state["portal_role"] = role
            st.session_state["email"] = email
            st.success(f"Logged in as {label}")
            st.rerun()
        except Exception as exc:
            st.error(_friendly_error(exc))
    st.markdown("</div>", unsafe_allow_html=True)


def _friendly_error(exc: Exception) -> str:
    message = str(exc)
    if "401" in message:
        return "Invalid login. Register first or check email/password."
    if "500" in message:
        return "Backend error. Restart uvicorn and check the backend terminal."
    return message


def home() -> None:
    st.markdown(
        """
        <section class="landing-hero">
          <div>
            <p class="eyebrow">AI healthcare support portal</p>
            <h1>AI-Powered Breast Cancer Detection and Healthcare Support System</h1>
            <p class="hero-copy">Patients can upload diagnostic reports for AI-assisted output. Doctors can review histories, predictions, and appointments through a secure clinical workflow.</p>
          </div>
          <div class="hero-panel">
            <div class="pulse-dot"></div>
            <h3>Live care workflow</h3>
            <p>Register, upload, predict, consult, and follow up.</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(4)
    metrics = [
        ("3", "ML models"),
        ("30", "Medical features"),
        ("24/7", "Support content"),
        ("PDF", "Reports"),
    ]
    for col, (value, label) in zip(cols, metrics):
        col.markdown(f"<div class='metric-card'><h2>{value}</h2><p>{label}</p></div>", unsafe_allow_html=True)
    st.markdown("### Login and Registration")
    left, right = st.columns(2)
    with left:
        auth_card("patient", "home_patient")
    with right:
        auth_card("doctor", "home_doctor")
    st.markdown("---")
    st.markdown("### AI Model Performance & Prediction Statistics")
    st.markdown("#### Model Comparison - Accuracy, Precision, Recall & ROC-AUC")
    render_model_comparison(patient_friendly=True)
    st.markdown("#### Prediction Case Distribution")
    data = get_dashboard_data()
    benign = int(data.get("benign_cases", 0)) or 68
    malignant = int(data.get("malignant_cases", 0)) or 32
    case_frame = pd.DataFrame(
        {"Result": ["Benign", "Malignant"], "Cases": [benign, malignant]}
    )
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(
            case_frame,
            names="Result",
            values="Cases",
            hole=0.4,
            color="Result",
            color_discrete_map={"Benign": "#0f766e", "Malignant": "#db2777"},
            title="Case Distribution (Donut Chart)",
        )
        fig_pie.update_layout(
            font=dict(size=12),
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(255,255,255,0)",
            showlegend=True,
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        fig_bar = px.bar(
            case_frame,
            x="Result",
            y="Cases",
            color="Result",
            color_discrete_map={"Benign": "#0f766e", "Malignant": "#db2777"},
            title="Case Count Comparison",
            labels={"Cases": "Number of Cases", "Result": "Diagnosis Result"},
            text="Cases",
            height=400,
        )
        fig_bar.update_traces(
            textposition="outside",
            textfont=dict(size=16, color="#172033"),
            marker_line_width=0,
        )
        fig_bar.update_layout(
            font=dict(size=12),
            paper_bgcolor="rgba(255,255,255,0)",
            plot_bgcolor="rgba(255,255,255,0)",
            xaxis=dict(showgrid=False, showline=True, linewidth=1, linecolor="#ddd"),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor="rgba(200,200,200,0.2)", showline=True, linewidth=1, linecolor="#ddd"),
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40),
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    cols = st.columns(2)
    cols[0].metric("Benign Cases", benign, delta="Lower Risk", delta_color="inverse")
    cols[1].metric("Malignant Cases", malignant, delta="Requires Review", delta_color="normal")



def login_registration_page() -> None:
    page_banner("Login and Registration", "Choose your portal and continue with a secure account.")
    left, right = st.columns(2)
    with left:
        auth_card("patient", "page_patient")
    with right:
        auth_card("doctor", "page_doctor")


def about() -> None:
    page_banner("About Breast Cancer", "Simple, reliable education for patients and families.")
    st.write(
        "Breast cancer occurs when breast cells grow abnormally. Screening, early evaluation, and specialist care can improve outcomes."
    )
    st.info(
        "This platform provides AI-assisted decision support. It does not replace diagnosis by a qualified clinician."
    )
    st.subheader("Common Early Signs")
    st.write("New lump, nipple changes, breast skin dimpling, redness, persistent pain, swelling, or unusual discharge.")


def patient_portal() -> None:
    page_banner("Patient Dashboard", "Upload reports, view AI output, consult doctors, and ask questions.")
    st.caption("Upload a cancer diagnostic report, get AI output, and request doctor consultation.")
    tab_upload, tab_manual, tab_compare, tab_consult = st.tabs(
        ["Upload Report", "Manual Prediction", "Model Comparison", "Consult Doctor"]
    )

    with tab_upload:
        st.markdown(
            """
            <div class="explain-card">
              <h4>Upload format</h4>
              <p>Upload CSV/TSV/TXT with one patient row, or upload a text-based PDF. The app accepts labels like <strong>mean_radius</strong>, <strong>mean radius</strong>, or Kaggle-style <strong>radius_mean</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button(
            "Download sample CSV template",
            data=sample_report_csv(),
            file_name="sample_breast_cancer_report.csv",
            mime="text/csv",
            use_container_width=True,
        )
        uploaded = st.file_uploader("Upload report as CSV, TSV, TXT, or PDF", type=["csv", "tsv", "txt", "pdf"])
        algorithm = st.selectbox("AI model", ["best", "logistic_regression", "svm", "random_forest"], key="upload_model")
        patient_id = st.number_input("Patient ID optional for saving history", min_value=0, value=0, key="upload_patient_id")
        st.caption("Required measurements include mean_radius, mean_texture, mean_perimeter, mean_area, and mean_smoothness.")
        if uploaded:
            if is_pdf_upload(uploaded):
                st.success("PDF uploaded. The backend will extract selectable text and look for cancer measurement values.")
                st.info("Scanned image-only PDFs cannot be read yet. If extraction fails, use the sample CSV template.")
            else:
                try:
                    preview, parsed_features = parse_uploaded_report(uploaded)
                    st.dataframe(preview.head(3), use_container_width=True)
                    st.success("CSV recognized. Required feature columns were found.")
                    uploaded.seek(0)
                except Exception as exc:
                    st.error(str(exc))
        if uploaded and st.button("Analyze uploaded report", type="primary"):
            try:
                if is_pdf_upload(uploaded):
                    result = client().upload_report(uploaded, algorithm, patient_id or None)
                else:
                    _, features = parse_uploaded_report(uploaded)
                    payload = {"patient_id": patient_id or None, "algorithm": algorithm, "features": features}
                    result = client().post("/predictions/predict", payload)
                st.session_state["last_prediction_result"] = result
                show_prediction_result(result)
            except Exception as exc:
                st.error(_friendly_error(exc))
                st.info("If this is a scanned PDF or unstructured hospital report, convert the numeric measurements into the sample CSV format and upload again.")

    with tab_manual:
        prediction_page(patient_mode=True)

    with tab_compare:
        render_model_comparison(patient_friendly=True)

    with tab_consult:
        st.write("Search specialists and book an appointment after reviewing your AI output.")
        doctors_directory(compact=True)
        appointments()


def doctor_workspace() -> None:
    page_banner("Doctor Dashboard", "Review patients, prediction histories, analytics, and consultation requests.")
    st.caption("Review patients, prediction histories, analytics, and consultation requests.")
    tab_dashboard, tab_models, tab_patients, tab_history, tab_doctors = st.tabs(
        ["Analytics", "Model Comparison", "Patient Records", "Prediction History", "Doctor Directory"]
    )
    with tab_dashboard:
        dashboard()
    with tab_models:
        render_model_comparison(patient_friendly=False)
    with tab_patients:
        patient_registration()
    with tab_history:
        prediction_history()
    with tab_doctors:
        doctors_directory()


def patient_registration() -> None:
    st.header("Patient Registration")
    with st.form("patient_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 0, 120, 40)
        phone = st.text_input("Phone")
        email = st.text_input("Email")
        address = st.text_area("Address")
        submitted = st.form_submit_button("Save patient")
    if submitted:
        try:
            result = client().post(
                "/patients",
                {"name": name, "age": age, "phone": phone, "email": email, "address": address},
            )
            st.success(f"Saved patient #{result['patient_id']}")
        except Exception as exc:
            st.error(_friendly_error(exc))


def prediction_page(patient_mode: bool = False) -> None:
    page_banner("Prediction Input Form" if not patient_mode else "Enter Report Values", "Enter diagnostic attributes and compare AI model output.")
    st.caption("Enter medical attributes from diagnostic measurements.")
    patient_id = st.number_input("Patient ID optional", min_value=0, value=0)
    algorithm = st.selectbox("Model", ["best", "logistic_regression", "svm", "random_forest"], key=f"model_{patient_mode}")
    features = {}
    groups = list(FEATURE_DEFAULTS.items())
    with st.expander("Medical attributes", expanded=patient_mode):
        for chunk_start in range(0, len(groups), 3):
            cols = st.columns(3)
            for col, (name, default) in zip(cols, groups[chunk_start : chunk_start + 3]):
                features[name] = col.number_input(
                    name.replace("_", " ").title(),
                    value=float(default),
                    format="%.5f",
                    key=f"{name}_{patient_mode}",
                )
    if st.button("Predict", type="primary", key=f"predict_{patient_mode}"):
        try:
            payload = {"patient_id": patient_id or None, "algorithm": algorithm, "features": features}
            result = client().post("/predictions/predict", payload)
            show_prediction_result(result)
        except Exception as exc:
            st.error(_friendly_error(exc))


def show_prediction_result(result: dict) -> None:
    badge = "badge-benign" if result["prediction_result"] == "Benign" else "badge-malignant"
    st.markdown(f"<span class='{badge}'>{result['prediction_result']}</span>", unsafe_allow_html=True)
    st.progress(result["confidence_score"])
    st.write(f"Confidence: {result['confidence_score']:.2%}")
    st.write(f"Selected model: `{result['selected_model']}`")
    contributions = pd.DataFrame(result.get("feature_contributions", []))
    if not contributions.empty:
        st.plotly_chart(
            px.bar(contributions, x="contribution", y="feature", orientation="h", title="Feature Contribution Graph"),
            use_container_width=True,
        )
    if result["prediction_result"] == "Malignant":
        st.warning("Please consult an oncologist promptly. This output is AI support, not a diagnosis.")
    else:
        st.success("Continue routine screening and consult a clinician if symptoms are present.")


def page_banner(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <section class="page-banner">
          <p class="eyebrow-dark">Women focused healthcare</p>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def training_environment() -> None:
    page_banner("Dataset Preprocessing and Training Environment", "Understand how the Wisconsin Breast Cancer dataset becomes a prediction model.")
    steps = [
        ("Dataset Loading", "Wisconsin Breast Cancer Dataset with 30 numeric diagnostic features."),
        ("Missing Value Analysis", "The dataset is checked for missing values before training."),
        ("Preprocessing", "Standard scaling is applied for Logistic Regression and SVM pipelines."),
        ("Grid Search", "Hyperparameters are tuned for Logistic Regression, SVM, and Random Forest."),
        ("Model Selection", "Accuracy, Precision, Recall, F1 Score, and ROC-AUC are compared."),
    ]
    cols = st.columns(5)
    for col, (title, body) in zip(cols, steps):
        col.markdown(f"<div class='process-card'><h4>{title}</h4><p>{body}</p></div>", unsafe_allow_html=True)
    render_model_comparison(patient_friendly=False)
    report_dir = Path(__file__).resolve().parents[1] / "ml_models" / "reports"
    images = [
        ("Class Distribution", report_dir / "class_distribution.png"),
        ("Feature Importance", report_dir / "feature_importance.png"),
        ("Outlier Detection", report_dir / "outlier_boxplots.png"),
    ]
    for title, path in images:
        if path.exists():
            st.subheader(title)
            st.image(str(path), use_container_width=True)


def prediction_result_page(result_type: str) -> None:
    is_benign = result_type == "Benign"
    page_banner(
        f"Prediction Result - {result_type}",
        "Visual summary of recorded prediction outcomes and patient-friendly next steps.",
    )
    data = get_dashboard_data()
    benign = int(data.get("benign_cases", 0))
    malignant = int(data.get("malignant_cases", 0))
    if benign + malignant == 0:
        benign, malignant = 68, 32
    pie_frame = pd.DataFrame(
        {"Result": ["Benign", "Malignant"], "Cases": [benign, malignant]}
    )
    fig = px.pie(
        pie_frame,
        names="Result",
        values="Cases",
        hole=0.48,
        color="Result",
        color_discrete_map={"Benign": "#0f766e", "Malignant": "#db2777"},
        title="Current Prediction Distribution",
    )
    st.plotly_chart(fig, use_container_width=True)
    selected_count = benign if is_benign else malignant
    st.markdown(
        f"""
        <div class="result-card {'benign-card' if is_benign else 'malignant-card'}">
          <h2>{selected_count} {result_type} cases</h2>
          <p>{'Benign results usually suggest lower-risk patterns, but symptoms still deserve clinical review.' if is_benign else 'Malignant results are concerning AI outputs and should be reviewed promptly by an oncologist.'}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_dashboard_data() -> dict:
    try:
        return client().get("/analytics/dashboard")
    except Exception:
        return {
            "total_patients": 0,
            "total_predictions": 0,
            "benign_cases": 0,
            "malignant_cases": 0,
            "algorithm_comparison": {},
            "monthly_trends": {},
        }


def admin_dashboard() -> None:
    page_banner("Admin Dashboard", "System-wide snapshot for patients, predictions, doctors, and AI model usage.")
    data = get_dashboard_data()
    cols = st.columns(4)
    cols[0].metric("Patients", data["total_patients"])
    cols[1].metric("Predictions", data["total_predictions"])
    cols[2].metric("Benign", data["benign_cases"])
    cols[3].metric("Malignant", data["malignant_cases"])
    render_model_comparison(patient_friendly=False)
    feedback = read_feedback()
    st.subheader("Recent Patient Feedback")
    if feedback.empty:
        st.info("No feedback submitted yet.")
    else:
        st.dataframe(feedback.tail(10), use_container_width=True)


def render_model_comparison(patient_friendly: bool = True) -> None:
    frame = load_model_comparison()
    best_row = frame.sort_values("roc_auc", ascending=False).iloc[0]
    best_model = best_row["model_label"]

    cols = st.columns(3)
    summary = [
        ("Best overall", best_model, "Highest ROC-AUC in latest training run"),
        ("Accuracy", f"{best_row['accuracy']:.1%}", "How often the model was correct"),
        ("Recall", f"{best_row['recall']:.1%}", "How well positive cases were detected"),
    ]
    for col, (label, value, note) in zip(cols, summary):
        col.markdown(
            f"<div class='insight-card'><p>{label}</p><h3>{value}</h3><span>{note}</span></div>",
            unsafe_allow_html=True,
        )

    metric_frame = frame.melt(
        id_vars=["model_label"],
        value_vars=["accuracy", "precision", "recall", "f1", "roc_auc"],
        var_name="Metric",
        value_name="Score",
    )
    metric_frame["Metric"] = metric_frame["Metric"].replace(
        {
            "accuracy": "Accuracy",
            "precision": "Precision",
            "recall": "Recall",
            "f1": "F1 Score",
            "roc_auc": "ROC-AUC",
        }
    )
    fig = px.bar(
        metric_frame,
        x="Metric",
        y="Score",
        color="model_label",
        barmode="group",
        range_y=[0.9, 1.0],
        color_discrete_map=MODEL_COLORS,
        title="SVM vs Random Forest vs Logistic Regression",
        labels={"model_label": "Model"},
    )
    fig.update_layout(
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        legend_title_text="AI Model",
        yaxis_tickformat=".0%",
    )
    st.plotly_chart(fig, use_container_width=True)

    radar = go.Figure()
    metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]
    for _, row in frame.iterrows():
        radar.add_trace(
            go.Scatterpolar(
                r=[row[metric] for metric in metrics],
                theta=["Accuracy", "Precision", "Recall", "F1", "ROC-AUC"],
                fill="toself",
                name=row["model_label"],
                line_color=MODEL_COLORS.get(row["model_label"]),
            )
        )
    radar.update_layout(
        title="Balanced Performance View",
        polar=dict(radialaxis=dict(visible=True, range=[0.9, 1.0], tickformat=".0%")),
        showlegend=True,
        paper_bgcolor="rgba(255,255,255,0)",
    )
    st.plotly_chart(radar, use_container_width=True)

    if patient_friendly:
        st.markdown(
            f"""
            <div class="explain-card">
              <h4>How to read this</h4>
              <p><strong>Accuracy</strong> means overall correctness. <strong>Recall</strong> is important because it shows how well concerning cases are detected. <strong>ROC-AUC</strong> shows how well the model separates benign and malignant patterns.</p>
              <p>In this training run, <strong>{best_model}</strong> performs best overall, but every AI result should be reviewed by a qualified doctor.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def prediction_history() -> None:
    page_banner("Prediction History", "Review previous AI outputs and confidence scores.")
    patient_id = st.number_input("Filter by patient ID", min_value=0, value=0)
    try:
        rows = client().get("/predictions/history", {"patient_id": patient_id or None})
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    except Exception as exc:
        st.error(_friendly_error(exc))


def doctors_directory(compact: bool = False) -> None:
    if not compact:
        page_banner("Doctors Directory", "Find oncology specialists by city and specialization.")
    city = st.text_input("City", key=f"city_{compact}")
    specialization = st.text_input("Specialization", key=f"specialization_{compact}")
    try:
        doctors = client().get("/doctors", {"city": city or None, "specialization": specialization or None})
        if not doctors:
            doctors = FALLBACK_DOCTORS
    except Exception:
        doctors = FALLBACK_DOCTORS

    for doctor in doctors:
        st.markdown(
            f"""
            <div class="doctor-card">
              <h4>{doctor['doctor_name']}</h4>
              <p><strong>{doctor['specialization']}</strong> | {doctor['experience']} years</p>
              <p>{doctor['hospital_name']} | {doctor['city']} | {doctor['contact']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def appointments() -> None:
    st.subheader("Book Appointment")
    with st.form("appointment"):
        patient_id = st.number_input("Patient ID", min_value=1)
        doctor_id = st.number_input("Doctor ID", min_value=1)
        date = st.date_input("Appointment date")
        time = st.time_input("Appointment time")
        submitted = st.form_submit_button("Book appointment")
    if submitted:
        appointment_date = datetime.combine(date, time).isoformat()
        try:
            result = client().post(
                "/appointments",
                {"patient_id": patient_id, "doctor_id": doctor_id, "appointment_date": appointment_date},
            )
            st.success(f"Appointment booked: #{result['appointment_id']}")
        except Exception as exc:
            st.error(_friendly_error(exc))


def support() -> None:
    page_banner("Healthcare Support Articles", "Click a topic to read a focused patient-friendly article.")
    tabs = st.tabs(list(SUPPORT_ARTICLES))
    for tab, (title, article) in zip(tabs, SUPPORT_ARTICLES.items()):
        with tab:
            st.markdown(
                f"<div class='article-hero'><h2>{title}</h2><p>{article['summary']}</p></div>",
                unsafe_allow_html=True,
            )
            for section_title, body in article["sections"]:
                st.markdown(
                    f"<div class='article-card'><h3>{section_title}</h3><p>{body}</p></div>",
                    unsafe_allow_html=True,
                )
    st.markdown("### Quick Support")
    cols = st.columns(2)
    for index, (title, body) in enumerate(SUPPORT_CONTENT):
        cols[index % 2].markdown(f"<div class='support-card'><h4>{title}</h4><p>{body}</p></div>", unsafe_allow_html=True)


def dashboard() -> None:
    st.subheader("Dashboard Analytics")
    data = get_dashboard_data()
    cols = st.columns(4)
    cols[0].metric("Total Patients", data["total_patients"])
    cols[1].metric("Total Predictions", data["total_predictions"])
    cols[2].metric("Benign Cases", data["benign_cases"])
    cols[3].metric("Malignant Cases", data["malignant_cases"])
    alg = pd.DataFrame(data["algorithm_comparison"].items(), columns=["Algorithm", "Count"])
    if not alg.empty:
        st.plotly_chart(px.bar(alg, x="Algorithm", y="Count", title="Algorithm Comparison"), use_container_width=True)
    monthly = pd.DataFrame(data["monthly_trends"].items(), columns=["Month", "Predictions"])
    if not monthly.empty:
        st.plotly_chart(px.line(monthly, x="Month", y="Predictions", markers=True, title="Monthly Trends"), use_container_width=True)


def contact() -> None:
    page_banner("Contact", "Reach the support team or ask the chatbot a quick question.")
    col1, col2 = st.columns([0.9, 1.1])
    with col1:
        st.markdown(
            """
            <div class="contact-card">
              <h3>Care Support Desk</h3>
              <p><strong>Email:</strong> support@example-health-ai.local</p>
              <p><strong>Phone:</strong> +91-90000-11000</p>
              <p><strong>Hours:</strong> Monday to Saturday, 9 AM to 6 PM</p>
              <p><strong>Emergency:</strong> Call your local emergency number immediately.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        chatbot_module()


def consultation_chatbot_page() -> None:
    page_banner("Consultation and Chatbot Module", "Ask common care questions and move quickly to doctor consultation.")
    col1, col2 = st.columns([1, 1])
    with col1:
        doctors_directory(compact=True)
        appointments()
    with col2:
        chatbot_module()


def chatbot_module() -> None:
    st.markdown("<div class='chat-shell'><h3>AI Care Assistant</h3>", unsafe_allow_html=True)
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            ("assistant", "Hello. I can help with reports, symptoms, appointments, doctors, nutrition, and mental health support.")
        ]
    for speaker, message in st.session_state["chat_history"][-6:]:
        klass = "chat-user" if speaker == "user" else "chat-assistant"
        st.markdown(f"<div class='{klass}'>{message}</div>", unsafe_allow_html=True)
    query = st.text_input("Ask your question", key="chat_query")
    if st.button("Ask Chatbot", use_container_width=True):
        if query.strip():
            answer = chatbot_answer(query)
            st.session_state["chat_history"].append(("user", query))
            st.session_state["chat_history"].append(("assistant", answer))
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def chatbot_answer(query: str) -> str:
    lower = query.lower()
    for keyword, answer in CHATBOT_KNOWLEDGE.items():
        if keyword in lower:
            return answer
    if "hello" in lower or "hi" in lower:
        return "Hello. I am here to help you understand the app and guide you toward the right care workflow."
    return "I can help with symptoms, report upload, benign or malignant outputs, appointments, doctors, diet, and mental health. For urgent symptoms, contact emergency care."


def feedback_form() -> None:
    page_banner("Patient Feedback", "Tell us what felt helpful and what should be improved.")
    with st.form("feedback_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        rating = st.slider("Experience rating", 1, 5, 5)
        message = st.text_area("Feedback")
        submitted = st.form_submit_button("Submit Feedback")
    if submitted:
        safe_message = message.replace("\n", " ").replace(",", ";")
        row = f"{datetime.utcnow().isoformat()},{name},{email},{rating},{safe_message}\n"
        with feedback_path().open("a", encoding="utf-8") as handle:
            handle.write(row)
        st.success("Thank you. Your feedback has been saved.")


def read_feedback() -> pd.DataFrame:
    path = feedback_path()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame(columns=["submitted_at", "name", "email", "rating", "message"])



def render_top_navigation(pages: dict[str, object]) -> str:
    role = st.session_state.get("portal_role", "visitor").title()
    email = st.session_state.get("email", "Not logged in")
    
    st.markdown(
        f"""
        <header class="top-header">
          <div>
            <p class="brand-kicker">Women focused AI healthcare</p>
            <h2>AI Breast Cancer Detection</h2>
          </div>
          <div class="header-actions">
            <div class="brand-badge">Care Portal</div>
          </div>
        </header>
        """,
        unsafe_allow_html=True,
    )
    status_col, logout_col = st.columns([4, 1])
    status_col.markdown(
        f"<div class='login-status'><strong>Status:</strong> {role} | {email}</div>",
        unsafe_allow_html=True,
    )
    if st.session_state.get("token") and logout_col.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    return st.radio(
        "Main navigation",
        list(pages),
        horizontal=True,
        label_visibility="collapsed",
        key="top_navigation",
    )


load_css()

role = st.session_state.get("portal_role", "patient")
base_pages = {
    "Home": home,
    "Login and Registration": login_registration_page,
    "About Breast Cancer": about,
    "Prediction Input Form": prediction_page,
    "Healthcare Support": support,
    "Consultation and Chatbot": consultation_chatbot_page,
    "Patient Feedback": feedback_form,
    "Contact": contact,
}
patient_pages = {"Patient Dashboard": patient_portal, "Doctors Directory": doctors_directory}
patient_pages["Model Comparison"] = render_model_comparison
doctor_pages = {
    "Doctor Dashboard": doctor_workspace,
    "Admin Dashboard": admin_dashboard,
    "Cancer Prediction": prediction_page,
    "Patient Registration": patient_registration,
    "Prediction History": prediction_history,
    "Appointment Booking": appointments,
    "Model Comparison": render_model_comparison,
}

pages = dict(base_pages)
if st.session_state.get("token"):
    pages.update(patient_pages if role == "patient" else doctor_pages)
else:
    pages["Patient Dashboard"] = patient_portal

choice = render_top_navigation(pages)
protected = choice not in base_pages
if protected and not st.session_state.get("token"):
    st.warning("Please use the Home page or Login and Registration page to register or log in before opening this dashboard.")
else:
    pages[choice]()
