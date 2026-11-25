from unittest.mock import patch, MagicMock
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from services.user_service import (
    create_user,
    authenticate_user,
    get_user_by_id,
    initialize_user_indexes
)


USER_ID = ObjectId()

USER_DATA = {
    "name": "Matheus Rodrigues",
    "email": "matheus@email.com",
    "password": "SenhaSegura123"
}


@patch("services.user_service.collection.insert_one")
def test_criar_usuario_com_sucesso(mock_insert):
    mock_insert.return_value.inserted_id = USER_ID

    user = create_user(USER_DATA)

    assert user["_id"] == str(USER_ID)
    assert user["name"] == USER_DATA["name"]
    assert user["email"] == USER_DATA["email"]
    assert user["email_verified"] is False

    mock_insert.assert_called_once()


@patch("services.user_service.collection.insert_one")
def test_senha_e_armazenada_com_hash(mock_insert):
    mock_insert.return_value.inserted_id = USER_ID

    create_user(USER_DATA)

    saved_user = mock_insert.call_args.args[0]

    assert saved_user["password_hash"] != USER_DATA["password"]
    assert check_password_hash(
        saved_user["password_hash"],
        USER_DATA["password"]
    )


@patch("services.user_service.collection.insert_one")
def test_resposta_nao_contem_senha_ou_hash(mock_insert):
    mock_insert.return_value.inserted_id = USER_ID

    user = create_user(USER_DATA)

    assert "password" not in user
    assert "password_hash" not in user


@patch("services.user_service.collection.find_one")
def test_autenticar_usuario_com_senha_correta(mock_find):
    mock_find.return_value = {
        "_id": USER_ID,
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "password_hash": generate_password_hash("SenhaSegura123"),
        "email_verified": False
    }

    user = authenticate_user(
        "matheus@email.com",
        "SenhaSegura123"
    )

    assert user is not None
    assert user["_id"] == str(USER_ID)
    assert user["email"] == "matheus@email.com"


@patch("services.user_service.collection.find_one")
def test_rejeitar_senha_incorreta(mock_find):
    mock_find.return_value = {
        "_id": USER_ID,
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "password_hash": generate_password_hash("SenhaSegura123"),
        "email_verified": False
    }

    user = authenticate_user(
        "matheus@email.com",
        "SenhaErrada123"
    )

    assert user is None


@patch("services.user_service.collection.find_one")
def test_autenticacao_com_usuario_inexistente(mock_find):
    mock_find.return_value = None

    user = authenticate_user(
        "inexistente@email.com",
        "SenhaSegura123"
    )

    assert user is None


@patch("services.user_service.collection.find_one")
def test_email_e_normalizado_na_autenticacao(mock_find):
    mock_find.return_value = None

    authenticate_user(
        "  MATHEUS@EMAIL.COM  ",
        "SenhaSegura123"
    )

    mock_find.assert_called_once_with({
        "email": "matheus@email.com"
    })


@patch("services.user_service.collection.find_one")
def test_buscar_usuario_por_id_valido(mock_find):
    mock_find.return_value = {
        "_id": USER_ID,
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "email_verified": False,
        "created_at": None
    }

    user = get_user_by_id(str(USER_ID))

    assert user is not None
    assert user["_id"] == str(USER_ID)
    assert user["email"] == "matheus@email.com"


@patch("services.user_service.collection.find_one")
def test_buscar_usuario_inexistente(mock_find):
    mock_find.return_value = None

    user = get_user_by_id(str(USER_ID))

    assert user is None


def test_buscar_usuario_com_id_invalido():
    user = get_user_by_id("id-invalido")

    assert user is None


@patch("services.user_service.collection.create_index")
def test_inicializar_indice_unico_de_email(mock_create_index):
    initialize_user_indexes()

    mock_create_index.assert_called_once_with(
        "email",
        unique=True
    )
