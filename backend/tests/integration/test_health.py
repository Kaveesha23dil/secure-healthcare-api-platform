from fastapi.testclient import TestClient


def test_health_is_public_and_minimal(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["x-request-id"]


def test_ready_reports_database_availability_safely(client: TestClient, monkeypatch) -> None:
    import app.main

    class Context:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def execute(self, *args):
            return None

    monkeypatch.setattr(app.main, "SessionLocal", lambda: Context())
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
