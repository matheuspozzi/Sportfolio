from services.athlete_access_service import has_permission


def check_athlete_permission(user_id, athlete_id, permission):
    """
    Verifica se um usuário possui determinada permissão
    sobre um perfil de atleta.
    """

    allowed = has_permission(
        user_id=user_id,
        athlete_id=athlete_id,
        permission=permission
    )

    if not allowed:
        return False

    return True