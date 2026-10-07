from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_validation_error():
    payload = {
        "recipients": [
            {
                "recipient_name": "Test User",
                "recipient_email": "not-an-email",
                "course_name": "Python",
                "issue_date": "2026-10-07"
            }
        ]
    }
    res = client.post("/api/certificates/generate", json=payload)
    assert res.status_code == 422

def test_bulk_generation_and_retrieval():
    payload = {
        "recipients": [
            {
                "recipient_name": "John Doe",
                "recipient_email": "john@example.com",
                "course_name": "FastAPI Masterclass",
                "issue_date": "2026-10-07"
            },
            {
                "recipient_name": "Invalid Candidate",
                "recipient_email": "invalid@example.com",
                "course_name": "FastAPI Masterclass",
                "issue_date": "2026-10-07"
            }
        ]
    }
    
    res = client.post("/api/certificates/generate", json=payload)
    assert res.status_code == 200
    data = res.json()
    
    assert data["total_count"] == 2
    assert data["success_count"] == 1
    assert data["failed_count"] == 1

    job_id = data["job_id"]
    valid_item_id = None

    for item in data["items"]:
        if item["recipient_name"] == "John Doe":
            assert item["status"] == "SUCCESS"
            valid_item_id = item["id"]
        if item["recipient_name"] == "Invalid Candidate":
            assert item["status"] == "FAILED"

    status_res = client.get(f"/api/certificates/jobs/{job_id}")
    assert status_res.status_code == 200

    dl_res = client.get(f"/api/certificates/download/{valid_item_id}")
    assert dl_res.status_code == 200
    assert dl_res.headers["content-type"] == "application/pdf"