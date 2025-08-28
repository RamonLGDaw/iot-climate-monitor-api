
from fastapi.testclient import TestClient
from main import app  # Asegúrate de que 'main.py' tiene la instancia FastAPI llamada 'app'
from config.settings import settings

client = TestClient(app)


def test_health_check():
    print("DB URL in test:", settings.DATABASE_URL)
    response = client.get("/health_check")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["db"] == "connected"