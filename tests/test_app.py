import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Teste de listagem de atividades

def test_get_activities():
    # Arrange
    # Nenhuma preparação extra, pois usamos o banco em memória
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Teste de cadastro de participante com sucesso

def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Cleanup: remover o participante
    client.post(f"/activities/{activity}/unregister?email={email}")

# Teste de cadastro duplicado

def test_signup_duplicate():
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    # Arrange: garantir que está cadastrado
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={email}")

# Teste de remoção de participante

def test_unregister_success():
    activity = "Chess Club"
    email = "testuser3@mergington.edu"
    # Arrange: garantir que está cadastrado
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

# Teste de remoção de participante não cadastrado

def test_unregister_not_registered():
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]

# Teste de cadastro em atividade inexistente

def test_signup_nonexistent_activity():
    activity = "Nonexistent Activity"
    email = "testuser@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

# Teste de remoção em atividade inexistente

def test_unregister_nonexistent_activity():
    activity = "Nonexistent Activity"
    email = "testuser@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
