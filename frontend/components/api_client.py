from __future__ import annotations

import os
from typing import Any

import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


class ApiClient:
    def __init__(self, token: str | None = None):
        self.token = token

    @property
    def headers(self) -> dict[str, str]:
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    def register(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._post("/auth/register", payload)

    def login(self, email: str, password: str) -> str:
        return self._post("/auth/login", {"email": email, "password": password})["access_token"]

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        response = requests.get(f"{API_BASE_URL}{path}", params=params, headers=self.headers, timeout=20)
        self._raise_for_status(response)
        return response.json()

    def post(self, path: str, payload: dict[str, Any]) -> Any:
        return self._post(path, payload)

    def put(self, path: str, payload: dict[str, Any]) -> Any:
        response = requests.put(f"{API_BASE_URL}{path}", json=payload, headers=self.headers, timeout=20)
        self._raise_for_status(response)
        return response.json()

    def delete(self, path: str) -> None:
        response = requests.delete(f"{API_BASE_URL}{path}", headers=self.headers, timeout=20)
        self._raise_for_status(response)

    def upload_report(self, file_obj: Any, algorithm: str, patient_id: int | None = None) -> Any:
        data = {"algorithm": algorithm}
        if patient_id:
            data["patient_id"] = str(patient_id)
        files = {"file": (file_obj.name, file_obj.getvalue(), file_obj.type or "text/csv")}
        response = requests.post(
            f"{API_BASE_URL}/predictions/upload-report",
            data=data,
            files=files,
            headers=self.headers,
            timeout=30,
        )
        self._raise_for_status(response)
        return response.json()

    def _post(self, path: str, payload: dict[str, Any]) -> Any:
        response = requests.post(f"{API_BASE_URL}{path}", json=payload, headers=self.headers, timeout=20)
        self._raise_for_status(response)
        return response.json()

    @staticmethod
    def _raise_for_status(response: requests.Response) -> None:
        if response.ok:
            return
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"{response.status_code} error: {detail}")
