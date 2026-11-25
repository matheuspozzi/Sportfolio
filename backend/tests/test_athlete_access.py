
from unittest.mock import patch
from bson import ObjectId

from services.athlete_access_service import (
    is_primary_responsible,
    has_permission,
    serialize_access,
    create_access,
    get_user_access_for_athlete,
    list_athlete_access
)


USER_ID = str(ObjectId())
ATHLETE_ID = str(ObjectId())


@patch("services.athlete_access_service.collection.find_one")
def test_responsavel_principal_tem_permissao(mock_find_one):
    mock_find_one.return_value = {"is_primary": True}

    resultado = is_primary_responsible(USER_ID, ATHLETE_ID)

    assert resultado is True


@patch("services.athlete_access_service.collection.find_one")
def test_usuario_sem_responsabilidade_principal(mock_find_one):
    mock_find_one.return_value = None

    resultado = is_primary_responsible(USER_ID, ATHLETE_ID)

    assert resultado is False


def test_usuario_com_id_invalido():
    resultado = is_primary_responsible("id-invalido", ATHLETE_ID)

    assert resultado is False


def test_atleta_com_id_invalido():
    resultado = is_primary_responsible(USER_ID, "id-invalido")

    assert resultado is False



from unittest.mock import patch
from flask_jwt_extended import create_access_token


ATHLETE_ID = "507f1f77bcf86cd799439011"


def gerar_token(client, user_id):
    with client.application.app_context():
        token = create_access_token(identity=user_id)

    return token


@patch("routes.athletes.delete_athlete")
@patch("routes.athletes.is_primary_responsible")
def test_responsavel_principal_pode_excluir(
    mock_responsavel,
    mock_delete,
    client
):
    mock_responsavel.return_value = True
    mock_delete.return_value = True

    token = gerar_token(client, "507f1f77bcf86cd799439012")

    response = client.delete(
        f"/api/athletes/{ATHLETE_ID}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    mock_delete.assert_called_once_with(ATHLETE_ID)


@patch("routes.athletes.is_primary_responsible")
def test_usuario_sem_responsabilidade_nao_pode_excluir(
    mock_responsavel,
    client
):
    mock_responsavel.return_value = False

    token = gerar_token(client, "507f1f77bcf86cd799439013")

    response = client.delete(
        f"/api/athletes/{ATHLETE_ID}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403


@patch("routes.athletes.delete_athlete")
@patch("routes.athletes.is_primary_responsible")
def test_editor_nao_pode_excluir(
    mock_responsavel,
    mock_delete,
    client
):
    mock_responsavel.return_value = False

    token = gerar_token(client, "507f1f77bcf86cd799439014")

    response = client.delete(
        f"/api/athletes/{ATHLETE_ID}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    mock_delete.assert_not_called()


@patch("routes.athletes.delete_athlete")
@patch("routes.athletes.is_primary_responsible")
def test_visualizador_nao_pode_excluir(
    mock_responsavel,
    mock_delete,
    client
):
    mock_responsavel.return_value = False

    token = gerar_token(client, "507f1f77bcf86cd799439015")

    response = client.delete(
        f"/api/athletes/{ATHLETE_ID}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    mock_delete.assert_not_called()


@patch("routes.athletes.delete_athlete")
@patch("routes.athletes.is_primary_responsible")
def test_usuario_sem_acesso_nao_pode_excluir(
    mock_responsavel,
    mock_delete,
    client
):
    mock_responsavel.return_value = False

    token = gerar_token(client, "507f1f77bcf86cd799439016")

    response = client.delete(
        f"/api/athletes/{ATHLETE_ID}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 403
    mock_delete.assert_not_called()



def test_exclusao_com_id_invalido_retorna_400(client):
    token = gerar_token(client, "507f1f77bcf86cd799439012")

    response = client.delete(
        "/api/athletes/id-invalido",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400


@patch("routes.athletes.delete_athlete")
@patch("routes.athletes.is_primary_responsible")
def test_atleta_inexistente_retorna_404(
    mock_responsavel,
    mock_delete,
    client
):
    mock_responsavel.return_value = True
    mock_delete.return_value = False

    token = gerar_token(client, "507f1f77bcf86cd799439012")

    response = client.delete(
        f"/api/athletes/{ATHLETE_ID}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    mock_delete.assert_called_once_with(ATHLETE_ID)



import pytest


@patch("services.athlete_access_service.collection.find_one")
@pytest.mark.parametrize("permission", [
    "view",
    "edit",
    "manage_access"
])
def test_responsavel_principal_tem_todas_permissoes(
    mock_find_one,
    permission
):
    mock_find_one.return_value = {
        "is_primary": True,
        "permissions": {}
    }

    resultado = has_permission(
        USER_ID,
        ATHLETE_ID,
        permission
    )

    assert resultado is True


@patch("services.athlete_access_service.collection.find_one")
def test_editor_tem_permissoes_configuradas(mock_find_one):
    mock_find_one.return_value = {
        "is_primary": False,
        "permissions": {
            "view": True,
            "edit": True,
            "manage_access": False
        }
    }

    assert has_permission(USER_ID, ATHLETE_ID, "view") is True
    assert has_permission(USER_ID, ATHLETE_ID, "edit") is True
    assert has_permission(USER_ID, ATHLETE_ID, "manage_access") is False


@patch("services.athlete_access_service.collection.find_one")
def test_visualizador_pode_visualizar_mas_nao_editar(mock_find_one):
    mock_find_one.return_value = {
        "is_primary": False,
        "permissions": {
            "view": True,
            "edit": False,
            "manage_access": False
        }
    }

    assert has_permission(USER_ID, ATHLETE_ID, "view") is True
    assert has_permission(USER_ID, ATHLETE_ID, "edit") is False
    assert has_permission(USER_ID, ATHLETE_ID, "manage_access") is False


@patch("services.athlete_access_service.collection.find_one")
def test_usuario_sem_vinculo_nao_tem_permissao(mock_find_one):
    mock_find_one.return_value = None

    resultado = has_permission(USER_ID, ATHLETE_ID, "view")

    assert resultado is False


@patch("services.athlete_access_service.collection.find_one")
def test_vinculo_inativo_nao_concede_permissao(mock_find_one):
    mock_find_one.return_value = None

    resultado = has_permission(USER_ID, ATHLETE_ID, "view")

    assert resultado is False


def test_has_permission_com_usuario_invalido():
    assert has_permission("id-invalido", ATHLETE_ID, "view") is False


def test_has_permission_com_atleta_invalido():
    assert has_permission(USER_ID, "id-invalido", "view") is False


def test_serialize_access_converte_object_ids():
    access = {
        "_id": ObjectId(),
        "user_id": ObjectId(),
        "athlete_id": ObjectId(),
        "granted_by": ObjectId()
    }

    resultado = serialize_access(access)

    assert isinstance(resultado["_id"], str)
    assert isinstance(resultado["user_id"], str)
    assert isinstance(resultado["athlete_id"], str)
    assert isinstance(resultado["granted_by"], str)


def test_serialize_access_com_granted_by_nulo():
    access = {
        "_id": ObjectId(),
        "user_id": ObjectId(),
        "athlete_id": ObjectId(),
        "granted_by": None
    }

    resultado = serialize_access(access)

    assert resultado["granted_by"] is None

@patch("services.athlete_access_service.collection.insert_one")
def test_create_access_cria_vinculo_com_permissoes_padrao(mock_insert):
    novo_id = ObjectId()
    mock_insert.return_value.inserted_id = novo_id

    resultado = create_access(
        USER_ID,
        ATHLETE_ID,
        "guardian"
    )

    mock_insert.assert_called_once()

    assert resultado["_id"] == str(novo_id)
    assert resultado["user_id"] == USER_ID
    assert resultado["athlete_id"] == ATHLETE_ID
    assert resultado["role"] == "guardian"
    assert resultado["status"] == "active"
    assert resultado["is_primary"] is False

    assert resultado["permissions"] == {
        "view": True,
        "edit": False,
        "manage_access": False
    }


def test_create_access_rejeita_role_invalida():
    with pytest.raises(ValueError, match="Tipo de acesso inválido."):
        create_access(
            USER_ID,
            ATHLETE_ID,
            "administrador"
        )

@patch("services.athlete_access_service.collection.find_one")
def test_busca_vinculo_existente(mock_find_one):
    access_id = ObjectId()

    mock_find_one.return_value = {
        "_id": access_id,
        "user_id": ObjectId(USER_ID),
        "athlete_id": ObjectId(ATHLETE_ID),
        "role": "guardian",
        "status": "active",
        "is_primary": True
    }

    resultado = get_user_access_for_athlete(USER_ID, ATHLETE_ID)

    assert resultado["_id"] == str(access_id)
    assert resultado["user_id"] == USER_ID
    assert resultado["athlete_id"] == ATHLETE_ID
    assert resultado["role"] == "guardian"
    assert resultado["status"] == "active"


@patch("services.athlete_access_service.collection.find_one")
def test_busca_vinculo_inexistente(mock_find_one):
    mock_find_one.return_value = None

    resultado = get_user_access_for_athlete(USER_ID, ATHLETE_ID)

    assert resultado is None

@patch("services.athlete_access_service.collection.find")
def test_lista_vinculos_do_atleta(mock_find):
    access_1 = {
        "_id": ObjectId(),
        "user_id": ObjectId(),
        "athlete_id": ObjectId(ATHLETE_ID),
        "role": "guardian",
        "status": "active"
    }

    access_2 = {
        "_id": ObjectId(),
        "user_id": ObjectId(),
        "athlete_id": ObjectId(ATHLETE_ID),
        "role": "viewer",
        "status": "active"
    }

    mock_find.return_value.sort.return_value = [
        access_1,
        access_2
    ]

    resultado = list_athlete_access(ATHLETE_ID)

    assert len(resultado) == 2
    assert resultado[0]["role"] == "guardian"
    assert resultado[1]["role"] == "viewer"

    mock_find.assert_called_once_with({
        "athlete_id": ObjectId(ATHLETE_ID),
        "status": "active"
    })


@patch("services.athlete_access_service.collection.find")
def test_lista_vazia_quando_atleta_nao_tem_vinculos(mock_find):
    mock_find.return_value.sort.return_value = []

    resultado = list_athlete_access(ATHLETE_ID)

    assert resultado == []

@patch("services.athlete_access_service.collection.find_one")
def test_permissao_desconhecida_e_rejeitada(mock_find_one):
    mock_find_one.return_value = {
        "is_primary": True,
        "permissions": {}
    }

    resultado = has_permission(
        USER_ID,
        ATHLETE_ID,
        "delete_everything"
    )

    assert resultado is False
    mock_find_one.assert_not_called()


@patch("services.athlete_access_service.collection.insert_one")
def test_create_access_rejeita_permissao_desconhecida(mock_insert):
    with pytest.raises(ValueError, match="Permissão inválida."):
        create_access(
            USER_ID,
            ATHLETE_ID,
            "editor",
            permissions={
                "view": True,
                "delete_everything": True
            }
        )

    mock_insert.assert_not_called()


@patch("services.athlete_access_service.collection.insert_one")
def test_create_access_rejeita_valor_de_permissao_invalido(mock_insert):
    with pytest.raises(ValueError, match="Valor de permissão inválido."):
        create_access(
            USER_ID,
            ATHLETE_ID,
            "editor",
            permissions={
                "view": "sim",
                "edit": False,
                "manage_access": False
            }
        )

    mock_insert.assert_not_called()


from unittest.mock import patch
from flask_jwt_extended import create_access_token


@patch("routes.athletes.create_access")
@patch("routes.athletes.create_athlete")
def test_criar_atleta_com_sucesso(
    mock_create_athlete,
    mock_create_access,
    client
):
    atleta_id = str(ObjectId())

    mock_create_athlete.return_value = {
        "_id": atleta_id,
        "full_name": "João Silva",
        "birth_date": "2005-08-15",
        "modalities": ["futsal"]
    }

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.post(
        "/api/athletes",
        json={
            "full_name": "João Silva",
            "birth_date": "2005-08-15",
            "modalities": ["futsal"]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 201
    assert response.json["message"] == "Atleta cadastrado com sucesso."
    assert response.json["athlete"]["full_name"] == "João Silva"

    mock_create_athlete.assert_called_once()
    mock_create_access.assert_called_once()


@patch("routes.athletes.create_athlete")
def test_criar_atleta_sem_data_nascimento(mock_create_athlete, client):
    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.post(
        "/api/athletes",
        json={
            "full_name": "João Silva",
            "modalities": ["futsal"]
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 400
    assert response.json["error"] == "Data de nascimento é obrigatória."

    mock_create_athlete.assert_not_called()


def test_criar_atleta_sem_autenticacao(client):
    response = client.post(
        "/api/athletes",
        json={
            "full_name": "João Silva",
            "birth_date": "2005-08-15",
            "modalities": ["futsal"]
        }
    )

    assert response.status_code == 401


@patch("services.athlete_service.collection.find")
@patch("services.athlete_service.access_collection.find")
def test_listar_atletas_com_sucesso(
    mock_access_find,
    mock_athlete_find,
    client
):
    athlete_id = ObjectId()

    mock_access_find.return_value = [
        {"athlete_id": athlete_id}
    ]

    atleta = {
        "_id": athlete_id,
        "full_name": "João Silva",
        "birth_date": "2005-08-15",
        "modalities": ["futsal"]
    }

    mock_athlete_find.return_value.sort.return_value.limit.return_value = [
        atleta
    ]

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.get(
        "/api/athletes",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json["total"] == 1
    assert response.json["athletes"][0]["full_name"] == "João Silva"

    mock_access_find.assert_called_once()
    mock_athlete_find.assert_called_once()


@patch("routes.athletes.list_athletes")
def test_listar_atletas_sem_vinculos(mock_list_athletes, client):
    mock_list_athletes.return_value = []

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.get(
        "/api/athletes",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json["total"] == 0
    assert response.json["athletes"] == []

    mock_list_athletes.assert_called_once_with(USER_ID)


@patch("routes.athletes.get_athlete")
@patch("routes.athletes.check_athlete_permission")
def test_consultar_atleta_com_permissao(
    mock_permission,
    mock_get_athlete,
    client
):
    athlete_id = str(ObjectId())

    mock_permission.return_value = True

    mock_get_athlete.return_value = {
        "_id": athlete_id,
        "full_name": "João Silva",
        "birth_date": "2005-08-15",
        "modalities": ["futsal"]
    }

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.get(
        f"/api/athletes/{athlete_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json["athlete"]["full_name"] == "João Silva"

    mock_permission.assert_called_once()
    mock_get_athlete.assert_called_once_with(athlete_id)


@patch("routes.athletes.get_athlete")
@patch("routes.athletes.check_athlete_permission")
def test_consultar_atleta_sem_permissao(
    mock_permission,
    mock_get_athlete,
    client
):
    athlete_id = str(ObjectId())

    mock_permission.return_value = False

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.get(
        f"/api/athletes/{athlete_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403
    mock_permission.assert_called_once()
    mock_get_athlete.assert_not_called()


@patch("routes.athletes.get_athlete")
@patch("routes.athletes.check_athlete_permission")
def test_consultar_atleta_inexistente(
    mock_permission,
    mock_get_athlete,
    client
):
    athlete_id = str(ObjectId())

    mock_permission.return_value = True
    mock_get_athlete.return_value = None

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.get(
        f"/api/athletes/{athlete_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404
    mock_permission.assert_called_once()
    mock_get_athlete.assert_called_once_with(athlete_id)


@patch("routes.athletes.update_athlete")
@patch("routes.athletes.check_athlete_permission")
def test_editar_atleta_com_permissao(
    mock_permission,
    mock_update,
    client
):
    athlete_id = str(ObjectId())

    mock_permission.return_value = True
    mock_update.return_value = {
        "_id": athlete_id,
        "full_name": "João Silva Atualizado",
        "birth_date": "2005-08-15",
        "modalities": ["futsal"]
    }

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.patch(
        f"/api/athletes/{athlete_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "full_name": "João Silva Atualizado"
        }
    )

    assert response.status_code == 200
    assert response.json["athlete"]["full_name"] == "João Silva Atualizado"

    mock_permission.assert_called_once()
    mock_update.assert_called_once()


@patch("routes.athletes.update_athlete")
@patch("routes.athletes.check_athlete_permission")
def test_editar_atleta_com_permissao(
    mock_permission,
    mock_update,
    client
):
    athlete_id = str(ObjectId())

    mock_permission.return_value = True
    mock_update.return_value = {
        "_id": athlete_id,
        "full_name": "João Silva Atualizado",
        "birth_date": "2005-08-15",
        "modalities": ["futsal"]
    }

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.patch(
        f"/api/athletes/{athlete_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "full_name": "João Silva Atualizado"
        }
    )

    assert response.status_code == 200
    assert response.json["athlete"]["full_name"] == "João Silva Atualizado"

    mock_permission.assert_called_once()
    mock_update.assert_called_once()


@patch("routes.athletes.update_athlete")
@patch("routes.athletes.check_athlete_permission")
def test_editar_atleta_sem_permissao(
    mock_permission,
    mock_update,
    client
):
    athlete_id = str(ObjectId())

    mock_permission.return_value = False

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.patch(
        f"/api/athletes/{athlete_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "full_name": "João Silva Atualizado"
        }
    )

    assert response.status_code == 403
    mock_permission.assert_called_once()
    mock_update.assert_not_called()


@patch("routes.athletes.update_athlete")
@patch("routes.athletes.check_athlete_permission")
def test_editar_atleta_inexistente(
    mock_permission,
    mock_update,
    client
):
    athlete_id = str(ObjectId())

    mock_permission.return_value = True
    mock_update.return_value = None

    with client.application.app_context():
        token = create_access_token(identity=USER_ID)

    response = client.patch(
        f"/api/athletes/{athlete_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "full_name": "João Silva Atualizado"
        }
    )

    assert response.status_code == 404
    mock_permission.assert_called_once()
    mock_update.assert_called_once()
# Testes adicionais de cobertura das rotas de atletas

@patch("routes.athletes.create_access")
@patch("routes.athletes.create_athlete")
@patch("routes.athletes.delete_athlete")
def test_criar_atleta_com_falha_ao_vincular_responsavel(
    mock_delete,
    mock_create_athlete,
    mock_create_access,
    client
):
    athlete_id = str(ObjectId())

    mock_create_athlete.return_value = {
        "_id": athlete_id,
        "full_name": "João Silva"
    }

    mock_create_access.side_effect = Exception("Erro no vínculo")

    token = gerar_token(client, USER_ID)

    response = client.post(
        "/api/athletes",
        json={
            "full_name": "João Silva",
            "birth_date": "2005-08-15",
            "modalities": ["futsal"]
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 500
    assert response.json["error"] == "Não foi possível vincular o responsável ao atleta."
    mock_delete.assert_called_once_with(athlete_id)


def test_consultar_atleta_com_id_invalido(client):
    token = gerar_token(client, USER_ID)

    response = client.get(
        "/api/athletes/id-invalido",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json["error"] == "ID de atleta inválido."


def test_editar_atleta_com_id_invalido(client):
    token = gerar_token(client, USER_ID)

    response = client.patch(
        "/api/athletes/id-invalido",
        json={"full_name": "Novo nome"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json["error"] == "ID de atleta inválido."


@patch("routes.athletes.check_athlete_permission")
def test_editar_atleta_com_dados_vazios(mock_permission, client):
    mock_permission.return_value = True
    token = gerar_token(client, USER_ID)

    response = client.patch(
        f"/api/athletes/{ATHLETE_ID}",
        json={},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json["error"] == "Envie os dados que deseja atualizar."


@patch("routes.athletes.check_athlete_permission")
def test_editar_atleta_com_dados_invalidos(mock_permission, client):
    mock_permission.return_value = True
    token = gerar_token(client, USER_ID)

    response = client.patch(
        f"/api/athletes/{ATHLETE_ID}",
        json={"campo_inexistente": "valor"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert "Campos não permitidos" in response.json["error"]


@patch("routes.athletes.update_athlete")
@patch("routes.athletes.validate_athlete_data")
@patch("routes.athletes.check_athlete_permission")
def test_editar_atleta_sem_campos_validos(
    mock_permission,
    mock_validator,
    mock_update,
    client
):
    mock_permission.return_value = True
    mock_validator.return_value = ({}, None)

    token = gerar_token(client, USER_ID)

    response = client.patch(
        f"/api/athletes/{ATHLETE_ID}",
        json={"full_name": "João Silva"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json["error"] == "Nenhum campo permitido foi informado."
    mock_update.assert_not_called()


# Testes adicionais de cobertura do serviço de acesso

@patch("services.athlete_access_service.collection.create_index")
def test_inicializar_indices_de_acesso(mock_create_index):
    from services.athlete_access_service import initialize_indexes

    initialize_indexes()

    assert mock_create_index.call_count == 2

    mock_create_index.assert_any_call(
        [("user_id", 1), ("athlete_id", 1)],
        unique=True,
        partialFilterExpression={"status": "active"}
    )

    mock_create_index.assert_any_call(
        [("athlete_id", 1)],
        unique=True,
        partialFilterExpression={
            "status": "active",
            "is_primary": True
        }
    )


@patch("services.athlete_access_service.collection.insert_one")
def test_create_access_rejeita_permissoes_que_nao_sao_dicionario(mock_insert):
    with pytest.raises(
        ValueError,
        match="Permissões devem ser um dicionário."
    ):
        create_access(
            USER_ID,
            ATHLETE_ID,
            "editor",
            permissions=["view", "edit"]
        )

    mock_insert.assert_not_called()


@patch("services.athlete_access_service.collection.find_one")
def test_has_permission_rejeita_permissoes_em_formato_invalido(mock_find_one):
    mock_find_one.return_value = {
        "is_primary": False,
        "permissions": ["view", "edit"]
    }

    result = has_permission(
        USER_ID,
        ATHLETE_ID,
        "view"
    )

    assert result is False
    mock_find_one.assert_called_once()
