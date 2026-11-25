import pytest
from unittest.mock import patch
from bson import ObjectId
from flask_jwt_extended import create_access_token

from routes.users import users_bp


@pytest.fixture
def app():
    from flask import Flask

    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "chave-exclusiva-para-testes-somente-local-2026"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    from flask_jwt_extended import JWTManager
    JWTManager(app)

    app.register_blueprint(users_bp)

    return app


@pytest.fixture
def client(app):
    return app.test_client()


USER_ID = str(ObjectId())


@patch("routes.users.create_user")
def test_cadastrar_usuario_com_sucesso(mock_create_user, client):
    mock_create_user.return_value = {
        "_id": USER_ID,
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "email_verified": False
    }

    response = client.post(
        "/api/users/register",
        json={
            "name": "Matheus Rodrigues",
            "email": "matheus@email.com",
            "password": "SenhaSegura123"
        }
    )

    assert response.status_code == 201
    assert response.json["message"] == "Usuário cadastrado com sucesso."
    assert response.json["user"]["name"] == "Matheus Rodrigues"
    assert response.json["user"]["email"] == "matheus@email.com"

    mock_create_user.assert_called_once()


@patch("routes.users.create_user")
def test_cadastrar_usuario_com_email_duplicado(mock_create_user, client):
    from pymongo.errors import DuplicateKeyError

    mock_create_user.side_effect = DuplicateKeyError("E-mail duplicado")

    response = client.post(
        "/api/users/register",
        json={
            "name": "Matheus Rodrigues",
            "email": "matheus@email.com",
            "password": "SenhaSegura123"
        }
    )

    assert response.status_code == 409
    assert response.json["error"] == "Este e-mail já está cadastrado."


@patch("routes.users.create_user")
def test_cadastrar_usuario_sem_autenticacao(mock_create_user, client):
    mock_create_user.return_value = {
        "_id": USER_ID,
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "email_verified": False
    }

    response = client.post(
        "/api/users/register",
        json={
            "name": "Matheus Rodrigues",
            "email": "matheus@email.com",
            "password": "SenhaSegura123"
        }
    )

    assert response.status_code == 201


@patch("routes.users.create_user")
def test_cadastrar_usuario_com_dados_invalidos(mock_create_user, client):
    response = client.post(
        "/api/users/register",
        json={
            "name": "M",
            "email": "email-invalido",
            "password": "123"
        }
    )

    assert response.status_code == 400
    mock_create_user.assert_not_called()


@patch("routes.users.create_user")
def test_cadastrar_usuario_com_campo_nao_permitido(mock_create_user, client):
    response = client.post(
        "/api/users/register",
        json={
            "name": "Matheus Rodrigues",
            "email": "matheus@email.com",
            "password": "SenhaSegura123",
            "admin": True
        }
    )

    assert response.status_code == 400
    mock_create_user.assert_not_called()


@patch("routes.users.authenticate_user")
def test_login_com_sucesso(mock_authenticate, client):
    mock_authenticate.return_value = {
        "_id": USER_ID,
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "email_verified": False
    }

    response = client.post(
        "/api/users/login",
        json={
            "email": "matheus@email.com",
            "password": "SenhaSegura123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert response.json["user"]["email"] == "matheus@email.com"


@patch("routes.users.authenticate_user")
def test_login_com_senha_incorreta(mock_authenticate, client):
    mock_authenticate.return_value = None

    response = client.post(
        "/api/users/login",
        json={
            "email": "matheus@email.com",
            "password": "SenhaErrada123"
        }
    )

    assert response.status_code == 401
    assert response.json["error"] == "E-mail ou senha incorretos."


@patch("routes.users.authenticate_user")
def test_login_sem_dados_obrigatorios(mock_authenticate, client):
    response = client.post(
        "/api/users/login",
        json={
            "email": "matheus@email.com"
        }
    )

    assert response.status_code == 400
    mock_authenticate.assert_not_called()


@patch("routes.users.get_user_by_id")
def test_consultar_proprio_usuario(mock_get_user, client):
    mock_get_user.return_value = {
        "_id": USER_ID,
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "email_verified": False
    }

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.get(
        "/api/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json["user"]["email"] == "matheus@email.com"
    mock_get_user.assert_called_once_with(USER_ID)



@patch("routes.users.create_user")
def test_cadastro_com_erro_interno(mock_create_user, client):
    mock_create_user.side_effect = Exception("Erro interno")

    response = client.post(
        "/api/users/register",
        json={
            "name": "Matheus Rodrigues",
            "email": "matheus@email.com",
            "password": "SenhaSegura123"
        }
    )

    assert response.status_code == 500
    assert response.json["error"] == "Não foi possível cadastrar o usuário."


@patch("routes.users.authenticate_user")
def test_login_com_json_invalido(mock_authenticate, client):
    response = client.post(
        "/api/users/login",
        data="conteudo inválido",
        content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json["error"] == "Envie os dados em formato JSON."
    mock_authenticate.assert_not_called()


@patch("routes.users.get_user_by_id")
def test_consultar_usuario_inexistente(mock_get_user, client, app):
    mock_get_user.return_value = None

    with app.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json["error"] == "Usuário não encontrado."
    mock_get_user.assert_called_once_with(USER_ID)
