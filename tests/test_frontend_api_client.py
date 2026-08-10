from unittest.mock import (
    Mock,
    patch,
)

from frontend.services.api_client import (
    APIClient,
)


@patch(
    "frontend.services."
    "api_client.requests.get"
)
def test_get_health(
    mock_get,
):
    mock_response = Mock()

    mock_response.raise_for_status.return_value = (
        None
    )

    mock_response.json.return_value = {
        "status": "ok",
        "service": "obesity-risk-api",
    }

    mock_get.return_value = (
        mock_response
    )

    client = APIClient()

    result = (
        client.get_health()
    )

    assert (
        result["status"]
        == "ok"
    )

    assert (
        result["service"]
        == "obesity-risk-api"
    )

    mock_get.assert_called_once_with(
        "http://127.0.0.1:5000/health",
        timeout=5,
    )