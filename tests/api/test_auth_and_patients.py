def test_register_login_and_patient_crud(client, auth_headers):
    payload = {
        "name": "Jane Patient",
        "age": 45,
        "phone": "555-1000",
        "email": "jane@example.com",
        "address": "123 Care Street",
    }
    created = client.post("/api/v1/patients", json=payload, headers=auth_headers)
    assert created.status_code == 201
    patient_id = created.json()["patient_id"]

    fetched = client.get(f"/api/v1/patients/{patient_id}", headers=auth_headers)
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Jane Patient"

    updated = client.put(f"/api/v1/patients/{patient_id}", json={"age": 46}, headers=auth_headers)
    assert updated.status_code == 200
    assert updated.json()["age"] == 46

    deleted = client.delete(f"/api/v1/patients/{patient_id}", headers=auth_headers)
    assert deleted.status_code == 204

