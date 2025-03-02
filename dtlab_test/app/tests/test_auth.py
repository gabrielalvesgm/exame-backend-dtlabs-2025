#AUTHENTICATION TESTS#/app/tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_register_and_login():
    #Testing the registration of anew user
    register_payload = {
        "username": "TestUser02",
        "email": "TestUser02@test.com",
        "password": "testpassword"
    }
    response = client.post("auth/register", json=register_payload)
    assert response.status_code == 200, f"Registration failed: {response.text}"
    data = response.json()
    assert data["username"] == "TestUser02"
    assert data["email"] == "TestUser02@test.com"
    
    
    #Testing login with correct info
    login_payload = {
        "username": "TestUser02",
        "password": "testpassword"
    }
    response = client.post("auth/login", json=login_payload)
    assert response.status_code == 200, "Login failed: {response.text}"
    data =response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


#Testing login with invalid info
def test_login_with_invalid_credentials():
    #trying to login with wrong paswsord
    login_payload = {
        "username": "TestUser01",
        "password": "wrongpassword"
    }
    response = client.post("auth/login", json=login_payload)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json()
    assert data["detail"] == "Invalid username or password"