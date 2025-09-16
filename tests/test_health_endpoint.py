from fastapi.testclient import TestClient
from app.models import HealthCheckResponse, HealthStatus
from app.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200

    health_response = HealthCheckResponse.model_validate(response.json())
    assert health_response.status == HealthStatus.HEALTHY
