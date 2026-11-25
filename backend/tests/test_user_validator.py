from validators.user_validator import validate_user_data


def test_validar_usuario_com_dados_validos():
    data = {
        "name": " Matheus Rodrigues ",
        "email": " MATHEUS@EMAIL.COM ",
        "password": "SenhaSegura123"
    }

    result, error = validate_user_data(data)

    assert error is None
    assert result["name"] == "Matheus Rodrigues"
    assert result["email"] == "matheus@email.com"
    assert result["password"] == "SenhaSegura123"


def test_rejeitar_dados_que_nao_sao_dicionario():
    result, error = validate_user_data("dados inválidos")

    assert result is None
    assert error == "Envie os dados do usuário em formato JSON."


def test_rejeitar_campos_obrigatorios_ausentes():
    result, error = validate_user_data({
        "name": "Matheus"
    })

    assert result is None
    assert error == "Nome, e-mail e senha são obrigatórios."


def test_rejeitar_nome_invalido():
    result, error = validate_user_data({
        "name": "M",
        "email": "matheus@email.com",
        "password": "SenhaSegura123"
    })

    assert result is None
    assert error == "Informe um nome válido."


def test_rejeitar_nome_maior_que_120_caracteres():
    result, error = validate_user_data({
        "name": "A" * 121,
        "email": "matheus@email.com",
        "password": "SenhaSegura123"
    })

    assert result is None
    assert error == "O nome deve ter no máximo 120 caracteres."


def test_rejeitar_email_invalido():
    result, error = validate_user_data({
        "name": "Matheus Rodrigues",
        "email": "email-invalido",
        "password": "SenhaSegura123"
    })

    assert result is None
    assert error == "Informe um e-mail válido."


def test_rejeitar_email_maior_que_254_caracteres():
    result, error = validate_user_data({
        "name": "Matheus Rodrigues",
        "email": ("a" * 250) + "@email.com",
        "password": "SenhaSegura123"
    })

    assert result is None
    assert error == "Informe um e-mail válido."


def test_rejeitar_senha_que_nao_e_texto():
    result, error = validate_user_data({
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "password": 123456789012
    })

    assert result is None
    assert error == "Senha inválida."


def test_rejeitar_senha_menor_que_12_caracteres():
    result, error = validate_user_data({
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "password": "12345678901"
    })

    assert result is None
    assert error == "A senha deve ter pelo menos 12 caracteres."


def test_rejeitar_senha_maior_que_128_caracteres():
    result, error = validate_user_data({
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "password": "A" * 129
    })

    assert result is None
    assert error == "A senha deve ter no máximo 128 caracteres."


def test_rejeitar_campo_nao_permitido():
    result, error = validate_user_data({
        "name": "Matheus Rodrigues",
        "email": "matheus@email.com",
        "password": "SenhaSegura123",
        "admin": True
    })

    assert result is None
    assert error == "Foram enviados campos não permitidos."

def test_rejeitar_email_que_nao_e_texto():
    data = {
        "name": "Matheus Rodrigues",
        "email": 12345,
        "password": "SenhaSegura123"
    }

    result, error = validate_user_data(data)

    assert result is None
    assert error == "E-mail inválido."
