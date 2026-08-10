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


@patch(
    "frontend.services."
    "api_client.requests.post"
)
def test_predict(
    mock_post,
):
    mock_response = Mock()

    mock_response.raise_for_status.return_value = (
        None
    )

    mock_response.json.return_value = {
        "predicted_class":
            "Normal_Weight",

        "confidence":
            0.85,

        "probabilities": {
            "Insufficient_Weight":
                0.02,

            "Normal_Weight":
                0.85,

            "Overweight_Level_I":
                0.08,

            "Overweight_Level_II":
                0.03,

            "Obesity_Type_I":
                0.01,

            "Obesity_Type_II":
                0.005,

            "Obesity_Type_III":
                0.005,
        },
    }

    mock_post.return_value = (
        mock_response
    )

    payload = {
        "Age": 25.0,
        "Height": 1.70,
        "Weight": 70.0,
        "FCVC": 2.0,
        "NCP": 3.0,
        "CH2O": 2.0,
        "FAF": 1.0,
        "TUE": 1.0,
        "CAEC": "Sometimes",
        "CALC": "no",
        "Gender": "Male",
        "family_history_with_overweight":
            "yes",
        "FAVC": "yes",
        "SMOKE": "no",
        "SCC": "no",
        "MTRANS":
            "Public_Transportation",
    }

    client = APIClient()

    result = client.predict(
        payload
    )

    assert (
        result["predicted_class"]
        == "Normal_Weight"
    )

    assert (
        result["confidence"]
        == 0.85
    )

    assert (
        len(
            result[
                "probabilities"
            ]
        )
        == 7
    )

    assert (
        result[
            "probabilities"
        ][
            "Normal_Weight"
        ]
        == 0.85
    )

    mock_post.assert_called_once_with(
        "http://127.0.0.1:5000/predict",
        json=payload,
        timeout=5,
    )