#DATA TESTS #app/tests/test_data.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app) #new object from TestClient class

def test_post_data():
    payload = {
        "server_ulid": "01JMG0J6BH9JV08PKJD5GSRM84",
        "timestamp": "2025-01-01T01:01:01Z",
        "temperature": 30.0,
        "humidity": 30.0,
        "voltage": 220.0,
        "current": 1.5
    }
    
    response = client.post("/data", json=payload)
    assert response.status_code == 200 #Verify status code == 200(sucess)
    
    
def test_get_data():
    payload = {
        "server_ulid": "01JMG0J6BH9JV08PKJD5GSRM84",
        "timestamp": "2025-01-01T01:01:01Z",
        "temperature": 30.0,
        "humidity": 30.0,
        "voltage": 220.0,
        "current": 1.5
    }
    post_response = client.post("/data", json=payload)
    assert post_response.status_code == 200
    
    get_response = client.get("/data")
    assert get_response.status_code == 200
    
    
    data = get_response.json() #"Translates" response to JSON
    # Basic assertions to validate the response content
    # Assuming the endpoint returns a JSON with 'message' and 'data'
    assert "message" in data
    assert data["message"] == "Data retrieved"
    assert "data" in data
    assert len(data["data"]) >= 1 #Verify if there's at least 1 item in list
