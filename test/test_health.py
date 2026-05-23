import os

os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
)
os.environ.setdefault("JWT_SECRET", "test_secret")

from fastapi.testclient import TestClient
from app.main import app

# El test solo verifica el endpoint /health. Limpiamos el startup para que no
# dependa de una base de datos real durante la prueba.
app.router.on_startup.clear()

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["status"] == "ok"
