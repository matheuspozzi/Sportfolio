
from datetime import date

VALID_MODALITIES = {"futebol", "futsal"}
VALID_FEET = {"right", "left", "both"}

ALLOWED_FIELDS = {
    "full_name",
    "sport_name",
    "birth_date",
    "modalities",
    "position",
    "dominant_foot"
}


def validate_athlete_data(data, creating=False):
    if not isinstance(data, dict):
        return None, "Envie um JSON válido."

    if creating:
        if not data.get("full_name"):
            return None, "Nome completo é obrigatório."

        if not data.get("birth_date"):
            return None, "Data de nascimento é obrigatória."

        if not data.get("modalities"):
            return None, "Informe pelo menos uma modalidade."

    unknown_fields = set(data.keys()) - ALLOWED_FIELDS

    if unknown_fields:
        return None, f"Campos não permitidos: {', '.join(sorted(unknown_fields))}"

    validated = {}

    for field, value in data.items():

        if field in {"full_name", "sport_name", "position"}:
            if value is not None and not isinstance(value, str):
                return None, f"{field} deve ser um texto."

            if field == "full_name":
                if not isinstance(value, str) or not value.strip():
                    return None, "Nome completo é obrigatório."

                value = value.strip()

            elif isinstance(value, str):
                value = value.strip()

        elif field == "birth_date":
            if not isinstance(value, str):
                return None, "Data de nascimento deve estar no formato AAAA-MM-DD."

            try:
                parsed_date = date.fromisoformat(value)
            except ValueError:
                return None, "Data de nascimento inválida. Utilize AAAA-MM-DD."

            if parsed_date > date.today():
                return None, "A data de nascimento não pode ser futura."

            value = parsed_date.isoformat()

        elif field == "modalities":
            if not isinstance(value, list) or not value:
                return None, "Informe pelo menos uma modalidade."

            if not all(
                isinstance(item, str) and item in VALID_MODALITIES
                for item in value
            ):
                return None, "Modalidade inválida."

            value = list(dict.fromkeys(value))

        elif field == "dominant_foot":
            if value is not None and (
                not isinstance(value, str) or value not in VALID_FEET
            ):
                return None, "Pé dominante inválido."

        validated[field] = value

    return validated, None
