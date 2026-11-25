from datetime import date, timedelta

from validators.athlete_validator import validate_athlete_data


def dados_validos():
    return {
        "full_name": " Matheus Rodrigues ",
        "birth_date": "2005-05-15",
        "modalities": ["futebol", "futsal"],
        "sport_name": " Matheus ",
        "position": " Atacante ",
        "dominant_foot": "right"
    }


def test_validar_atleta_com_dados_validos():
    result, error = validate_athlete_data(dados_validos(), creating=True)

    assert error is None
    assert result["full_name"] == "Matheus Rodrigues"
    assert result["sport_name"] == "Matheus"
    assert result["position"] == "Atacante"


def test_rejeitar_dados_que_nao_sao_dicionario():
    result, error = validate_athlete_data("dados inválidos")

    assert result is None
    assert error == "Envie um JSON válido."


def test_rejeitar_nome_completo_ausente():
    data = dados_validos()
    data.pop("full_name")

    result, error = validate_athlete_data(data, creating=True)

    assert result is None
    assert error == "Nome completo é obrigatório."


def test_rejeitar_data_de_nascimento_ausente():
    data = dados_validos()
    data.pop("birth_date")

    result, error = validate_athlete_data(data, creating=True)

    assert result is None
    assert error == "Data de nascimento é obrigatória."


def test_rejeitar_modalidade_ausente():
    data = dados_validos()
    data.pop("modalities")

    result, error = validate_athlete_data(data, creating=True)

    assert result is None
    assert error == "Informe pelo menos uma modalidade."


def test_rejeitar_campo_nao_permitido():
    data = dados_validos()
    data["admin"] = True

    result, error = validate_athlete_data(data)

    assert result is None
    assert error == "Campos não permitidos: admin"


def test_rejeitar_nome_com_tipo_invalido():
    data = dados_validos()
    data["full_name"] = 123

    result, error = validate_athlete_data(data)

    assert result is None
    assert error == "full_name deve ser um texto."


def test_rejeitar_data_de_nascimento_invalida():
    data = dados_validos()
    data["birth_date"] = "15/05/2005"

    result, error = validate_athlete_data(data)

    assert result is None
    assert error == "Data de nascimento inválida. Utilize AAAA-MM-DD."


def test_rejeitar_data_de_nascimento_futura():
    data = dados_validos()
    data["birth_date"] = (date.today() + timedelta(days=1)).isoformat()

    result, error = validate_athlete_data(data)

    assert result is None
    assert error == "A data de nascimento não pode ser futura."


def test_rejeitar_modalidade_invalida():
    data = dados_validos()
    data["modalities"] = ["basquete"]

    result, error = validate_athlete_data(data)

    assert result is None
    assert error == "Modalidade inválida."


def test_rejeitar_modalidades_que_nao_sao_lista():
    data = dados_validos()
    data["modalities"] = "futebol"

    result, error = validate_athlete_data(data)

    assert result is None
    assert error == "Informe pelo menos uma modalidade."


def test_remover_modalidades_duplicadas():
    data = dados_validos()
    data["modalities"] = ["futebol", "futsal", "futebol"]

    result, error = validate_athlete_data(data)

    assert error is None
    assert result["modalities"] == ["futebol", "futsal"]


def test_rejeitar_pe_dominante_invalido():
    data = dados_validos()
    data["dominant_foot"] = "center"

    result, error = validate_athlete_data(data)

    assert result is None
    assert error == "Pé dominante inválido."


def test_aceitar_atualizacao_parcial():
    data = {
        "position": "Meio-campo"
    }

    result, error = validate_athlete_data(data)

    assert error is None
    assert result == data


def test_aceitar_pe_dominante_nulo():
    data = dados_validos()
    data["dominant_foot"] = None

    result, error = validate_athlete_data(data)

    assert error is None
    assert result["dominant_foot"] is None

def test_rejeitar_nome_com_apenas_espacos():
    data = {
        "full_name": "   "
    }

    result, error = validate_athlete_data(data)

    assert result is None
    assert error == "Nome completo é obrigatório."


def test_rejeitar_data_de_nascimento_que_nao_e_texto():
    data = {
        "birth_date": 20050515
    }

    result, error = validate_athlete_data(data)

    assert result is None
    assert error == "Data de nascimento deve estar no formato AAAA-MM-DD."
