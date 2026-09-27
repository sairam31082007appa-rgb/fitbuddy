from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "FitBuddy" in response.text


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_dashboard():

    response = client.get(
        "/view-all-users"
    )

    assert response.status_code == 200

    assert "Coach Dashboard" in response.text