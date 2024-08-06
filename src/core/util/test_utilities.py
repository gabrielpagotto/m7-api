import uuid
from main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.engine import Engine
from src.core.dependency import get_db
from src.core.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite://"


def get_test_client(authenticate=True):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    import src.core.model

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    if authenticate:
        response = client.post("/auth/signup", json=TestUser.as_dict())
        response_json = response.json()
        client.headers = {"Authorization": f"Bearer {response_json['access_token']}"}

    return client


class TestUser:
    email = "develop@m7academy.com.br"
    password = "m7.123"

    @staticmethod
    def as_dict():
        return {"email": TestUser.email, "password": TestUser.password}
