
import re
from datetime import datetime, timezone


def validate_user_data(data):
    if not isinstance(data, dict):
        return None, "Envie os dados do usuário em formato JSON."

    allowed_fields = {
        "name",
        "email",
        "password"
    }

    unknown_fields = set(data.keys()) - allowed_fields

    if unknown_fields:
        return None, "Foram enviados campos não permitidos."

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return None, "Nome, e-mail e senha são obrigatórios."

    if not isinstance(name, str) or len(name.strip()) < 2:
        return None, "Informe um nome válido."

    if len(name.strip()) > 120:
        return None, "O nome deve ter no máximo 120 caracteres."

    if not isinstance(email, str):
        return None, "E-mail inválido."

    email = email.strip().lower()

    if len(email) > 254 or not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email
    ):
        return None, "Informe um e-mail válido."

    if not isinstance(password, str):
        return None, "Senha inválida."

    if len(password) < 12:
        return None, "A senha deve ter pelo menos 12 caracteres."

    if len(password) > 128:
        return None, "A senha deve ter no máximo 128 caracteres."

    validated_data = {
        "name": name.strip(),
        "email": email,
        "password": password
    }

    return validated_data, None
