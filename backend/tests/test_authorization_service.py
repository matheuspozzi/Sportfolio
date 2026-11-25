from unittest.mock import patch

from services.authorization_service import check_athlete_permission


@patch("services.authorization_service.has_permission")
def test_usuario_tem_permissao(mock_has_permission):
    mock_has_permission.return_value = True

    result = check_athlete_permission(
        user_id="usuario123",
        athlete_id="atleta123",
        permission="edit"
    )

    assert result is True

    mock_has_permission.assert_called_once_with(
        user_id="usuario123",
        athlete_id="atleta123",
        permission="edit"
    )


@patch("services.authorization_service.has_permission")
def test_usuario_nao_tem_permissao(mock_has_permission):
    mock_has_permission.return_value = False

    result = check_athlete_permission(
        user_id="usuario123",
        athlete_id="atleta123",
        permission="delete"
    )

    assert result is False

    mock_has_permission.assert_called_once_with(
        user_id="usuario123",
        athlete_id="atleta123",
        permission="delete"
    )
