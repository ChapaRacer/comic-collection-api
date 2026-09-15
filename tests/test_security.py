import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_sqli_injection_attempt():
    payload = {
        "username": "admin' OR '1'='1",
        "password": "password123"
    }
    response = client.post("/auth/login", data=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong credentials"