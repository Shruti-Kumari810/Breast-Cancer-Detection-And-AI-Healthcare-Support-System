from frontend.components.content import FEATURE_DEFAULTS


def test_prediction_without_patient_record(client, auth_headers):
    response = client.post(
        "/api/v1/predictions/predict",
        json={"algorithm": "best", "features": FEATURE_DEFAULTS},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body["prediction_result"] in {"Benign", "Malignant"}
    assert 0 <= body["confidence_score"] <= 1
    assert body["selected_model"]

