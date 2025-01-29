import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models.task import Task
from app.models.user import User

def test_create_task(client: TestClient, normal_user_token_headers: dict, session: Session):
    data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium",
        "status": "todo"
    }
    response = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content 