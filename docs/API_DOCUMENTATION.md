# API Documentation

Base URL: `/api/v1`

Authentication uses JWT bearer tokens.

## Authentication

- `POST /auth/register`: Create doctor/user account.
- `POST /auth/login`: Return JWT access token.

## Patients

- `POST /patients`: Create patient.
- `GET /patients`: List patients.
- `GET /patients/{patient_id}`: Get patient.
- `PUT /patients/{patient_id}`: Update patient.
- `DELETE /patients/{patient_id}`: Delete patient.

## Predictions

- `POST /predictions/predict`: Predict benign or malignant result using selected model.
- `POST /predictions/upload-report`: Upload CSV, TSV, or TXT report and predict from report features.
- `GET /predictions/history?patient_id=1`: Get prediction history.
- `POST /predictions/report`: Generate PDF report.

## Doctors

- `GET /doctors`: List doctors. Supports `city` and `specialization` filters.
- `GET /doctors/{doctor_id}`: Get doctor details.

## Appointments

- `POST /appointments`: Book appointment.
- `POST /appointments/{appointment_id}/cancel`: Cancel appointment.

## Health Resources

- `GET /resources`: List support resources. Supports `resource_type` filter.

## Analytics

- `GET /analytics/dashboard`: Total patients, predictions, benign cases, malignant cases, monthly trends, and algorithm comparison.
