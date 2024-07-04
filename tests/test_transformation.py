import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import app
from src.database.base import Base
from src.database.session import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_transformation_job(test_db):
    response = client.post(
        "/api/v1/transform",
        json={"extraction_job_id": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"

def test_get_transformation_status(test_db):
    response = client.post(
        "/api/v1/transform",
        json={"extraction_job_id": 1}
    )
    assert response.status_code == 200
    job_id = response.json()["id"]

    response = client.get(f"/api/v1/transform/status/{job_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_id
