# app/tests/test_data.py

from datetime import datetime, timedelta, timezone
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    username = "test"
    email = "test@test.com"
    password = "test"
    register_payload = {
        "username": username,
        "email": email,
        "password": password
    }
    #Attempt to register the user (ignore if already exists)
    response = client.post("/auth/register", json=register_payload)
    
    #Login to obtain the jwt token
    login_payload = {"username": username, "password": password}
    response = client.post("/auth/login", json=login_payload)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json().get("access_token")
    return token

def test_get_data_without_aggregation():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    #Create a server
    server_payload = {"server_name": "TestDataServer"}
    response = client.post("/servers/", json=server_payload, headers=headers)
    assert response.status_code == 200, f"Server creation failed: {response.text}"
    server_ulid = response.json()["server_ulid"]


    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    record1 = {
        "server_ulid": server_ulid,
        "timestamp": now.isoformat(),  #timestamp at the start of the minute
        "temperature": 20.0
    }
    record2 = {
        "server_ulid": server_ulid,
        "timestamp": (now + timedelta(seconds=30)).isoformat(),
        "temperature": 30.0
    }
    r1 = client.post("/data", json=record1)
    r2 = client.post("/data", json=record2)
    assert r1.status_code == 200, f"Data insert failed: {r1.text}"
    assert r2.status_code == 200, f"Data insert failed: {r2.text}"

    #Query without aggregation: using sensor_type
    start_time = now.isoformat()
    end_time = (now + timedelta(minutes=1)).isoformat()
    params = {
        "server_ulid": server_ulid,
        "start_time": start_time,
        "end_time": end_time,
        "sensor_type": "temperature"
    }
    query_response = client.get("/data", params=params, headers=headers)
    assert query_response.status_code == 200, f"GET /data failed: {query_response.text}"
    data = query_response.json()
    #Expect at least 2 records to be returned
    assert isinstance(data, list)
    assert len(data) >= 2

def test_get_data_with_aggregation():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    #Create a server
    server_payload = {"server_name": "TestDataServerAggregation"}
    response = client.post("/servers/", json=server_payload, headers=headers)
    assert response.status_code == 200, f"Server creation failed: {response.text}"
    server_ulid = response.json()["server_ulid"]

    #Set 'now' to the exact beginning of the minute
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    values = [10, 20, 30, 40]
    for i, val in enumerate(values):
        record = {
            "server_ulid": server_ulid,
            "timestamp": (now + timedelta(seconds=i * 10)).isoformat(),
            "temperature": float(val)
        }
        response = client.post("/data", json=record)
        assert response.status_code == 200, f"Data insert failed: {response.text}"

    #Query with aggregation (by min)
    params = {
        "server_ulid": server_ulid,
        "sensor_type": "temperature",
        "aggregation": "minute",
        "start_time": now.isoformat(),
        "end_time": (now + timedelta(seconds=59)).isoformat()
    }
    agg_response = client.get("/data", params=params, headers=headers)
    assert agg_response.status_code == 200, f"GET /data with aggregation failed: {agg_response.text}"
    agg_data = agg_response.json()
    #Expect a single group with the average
    assert isinstance(agg_data, list)
    assert len(agg_data) == 1, f"Expected one group, got {len(agg_data)} groups"
    expected_avg = sum(values) / len(values)  # (10+20+30+40)/4 = 25.0
    assert abs(agg_data[0]["value"] - expected_avg) < 0.01, f"Expected average {expected_avg}, got {agg_data[0]['value']}"
