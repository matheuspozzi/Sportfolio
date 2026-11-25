from unittest.mock import patch, MagicMock
from bson import ObjectId

from services.athlete_service import (
    serialize_athlete,
    create_athlete,
    list_athletes,
    get_athlete,
    update_athlete,
    delete_athlete
)


ATHLETE_ID = ObjectId()
USER_ID = ObjectId()

ATHLETE_DATA = {
    "name": "Atleta Teste",
    "birth_date": "2005-05-15"
}


def test_serializar_atleta_com_sucesso():
    athlete = {
        "_id": ATHLETE_ID,
        "name": "Atleta Teste"
    }

    result = serialize_athlete(athlete)

    assert result["_id"] == str(ATHLETE_ID)
    assert result["name"] == "Atleta Teste"


def test_serializar_atleta_nulo():
    assert serialize_athlete(None) is None


def test_serializar_atleta_nao_altera_documento_original():
    athlete = {
        "_id": ATHLETE_ID,
        "name": "Atleta Teste"
    }

    serialize_athlete(athlete)

    assert isinstance(athlete["_id"], ObjectId)


@patch("services.athlete_service.collection.insert_one")
def test_criar_atleta_com_sucesso(mock_insert):
    mock_insert.return_value.inserted_id = ATHLETE_ID

    with patch("services.athlete_service.collection.find_one") as mock_find:
        mock_find.return_value = {
            "_id": ATHLETE_ID,
            **ATHLETE_DATA
        }

        result = create_athlete(ATHLETE_DATA)

    mock_insert.assert_called_once()
    assert result["_id"] == str(ATHLETE_ID)
    assert result["name"] == "Atleta Teste"


@patch("services.athlete_service.access_collection.find")
@patch("services.athlete_service.collection.find")
def test_listar_atletas_com_sucesso(mock_find, mock_access_find):
    mock_access_find.return_value = [
        {"athlete_id": ATHLETE_ID}
    ]

    mock_find.return_value.sort.return_value.limit.return_value = [
        {
            "_id": ATHLETE_ID,
            "name": "Atleta Teste"
        }
    ]

    result = list_athletes(str(USER_ID))

    assert len(result) == 1
    assert result[0]["_id"] == str(ATHLETE_ID)


@patch("services.athlete_service.access_collection.find")
@patch("services.athlete_service.collection.find")
def test_listar_atletas_sem_vinculos(mock_find, mock_access_find):
    mock_access_find.return_value = []

    result = list_athletes(str(USER_ID))

    assert result == []
    mock_find.assert_called_once_with({"_id": {"$in": []}})


@patch("services.athlete_service.collection.find_one")
def test_buscar_atleta_existente(mock_find):
    mock_find.return_value = {
        "_id": ATHLETE_ID,
        "name": "Atleta Teste"
    }

    result = get_athlete(str(ATHLETE_ID))

    assert result is not None
    assert result["_id"] == str(ATHLETE_ID)


@patch("services.athlete_service.collection.find_one")
def test_buscar_atleta_inexistente(mock_find):
    mock_find.return_value = None

    result = get_athlete(str(ATHLETE_ID))

    assert result is None


@patch("services.athlete_service.collection.update_one")
@patch("services.athlete_service.get_athlete")
def test_atualizar_atleta_com_sucesso(mock_get, mock_update):
    mock_update.return_value.matched_count = 1
    mock_get.return_value = {
        "_id": str(ATHLETE_ID),
        "name": "Nome Atualizado"
    }

    result = update_athlete(
        str(ATHLETE_ID),
        {"name": "Nome Atualizado"}
    )

    assert result["name"] == "Nome Atualizado"
    mock_update.assert_called_once()


@patch("services.athlete_service.collection.update_one")
def test_atualizar_atleta_inexistente(mock_update):
    mock_update.return_value.matched_count = 0

    result = update_athlete(
        str(ATHLETE_ID),
        {"name": "Nome Atualizado"}
    )

    assert result is None


@patch("services.athlete_service.collection.delete_one")
@patch("services.athlete_service.access_collection.delete_many")
def test_excluir_atleta_com_sucesso(mock_delete_access, mock_delete):
    mock_delete.return_value.deleted_count = 1

    result = delete_athlete(str(ATHLETE_ID))

    assert result is True
    mock_delete.assert_called_once()
    mock_delete_access.assert_called_once()


@patch("services.athlete_service.collection.delete_one")
def test_excluir_atleta_inexistente(mock_delete):
    mock_delete.return_value.deleted_count = 0

    result = delete_athlete(str(ATHLETE_ID))

    assert result is False
