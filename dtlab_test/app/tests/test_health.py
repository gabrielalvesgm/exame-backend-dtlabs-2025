from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    username = "TestHealthUser"
    email = "testhealthuser@test.com"
    password = "testpassword"
    register_payload = {
        "username": username,
        "email": email,
        "password": password
    }
    # Try to register the user (ignore error if already exists)
    response = client.post("/auth/register", json=register_payload)
    if response.status_code not in (200, 400):
        raise Exception(f"Unexpected error during registration: {response.text}")
    # Login using static credentials
    login_payload = {"username": username, "password": password}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json().get("access_token")
    return token

def test_server_health_online():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    server_payload = {"server_name": "TestServerOnline"}
    response = client.post("/servers/", json=server_payload, headers=headers)
    assert response.status_code == 200, f"Server creation failed: {response.text}"
    server_data = response.json()
    server_ulid = server_data["server_ulid"]

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()
    sensor_payload = {
        "server_ulid": server_ulid,
        "timestamp": now_iso,
        "temperature": 10.0
    }
    sensor_response = client.post("/data", json=sensor_payload)
    assert sensor_response.status_code == 200, f"Sensor data insert failed: {sensor_response.text}"

    health_response = client.get(f"/health/{server_ulid}", headers=headers)
    assert health_response.status_code == 200, f"Health check failed: {health_response.text}"
    health_data = health_response.json()
    assert health_data["status"] == "online", f"Expected 'online', got {health_data['status']}"

def test_server_health_offline():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    server_payload = {"server_name": "TestServerOffline"}
    response = client.post("/servers/", json=server_payload, headers=headers)
    assert response.status_code == 200, f"Server creation failed: {response.text}"
    server_data = response.json()
    server_ulid = server_data["server_ulid"]

    # Insert an old timestamp simulating offline status
    old_time_iso = (datetime.now(timezone.utc) - timedelta(seconds=30)).isoformat()
    
    sensor_payload = {
        "server_ulid": server_ulid,
        "timestamp": old_time_iso,
        "temperature": 10.0
    }
    sensor_response = client.post("/data/", json=sensor_payload)
    assert sensor_response.status_code == 200, f"Sensor data insert failed: {sensor_response.text}"

    health_response = client.get(f"/health/{server_ulid}", headers=headers)
    assert health_response.status_code == 200, f"Health check failed: {health_response.text}"
    health_data = health_response.json()
    assert health_data["status"] == "offline", f"Expected 'offline', got {health_data['status']}"
    assert health_data["server_ulid"] == server_ulid
