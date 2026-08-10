from unittest.mock import (
    Mock,
    patch,
)

import pytest

from frontend.services.api_client import (
    APIClient,
    APIClientError,
)


@patch(
    "frontend.services."
    "api_client.requests.get"
)
def test_get_health(
    mock_get,
):
    mock_response = Mock()

    mock_response.ok = True
    mock_response.status_code = 200

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

    mock_response.ok = True
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "prediction_id": 1,

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
    }

    client = APIClient()

    result = (
        client.predict(
            payload
        )
    )

    assert (
        result["prediction_id"]
        == 1
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

    mock_post.assert_called_once_with(
        "http://127.0.0.1:5000/predict",
        json=payload,
        timeout=5,
    )


@patch(
    "frontend.services."
    "api_client.requests.get"
)
def test_get_predictions(
    mock_get,
):
    mock_response = Mock()

    mock_response.ok = True
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "count": 1,

        "predictions": [
            {
                "id": 1,

                "predicted_class":
                    "Normal_Weight",

                "confidence":
                    0.85,

                "model_name":
                    "Tuned Gradient Boosting",

                "scikit_learn_version":
                    "1.8.0",

                "created_at":
                    "2026-08-10 12:00:00",
            }
        ],
    }

    mock_get.return_value = (
        mock_response
    )

    client = APIClient()

    result = (
        client.get_predictions()
    )

    assert (
        result["count"]
        == 1
    )

    assert (
        result[
            "predictions"
        ][0]["id"]
        == 1
    )

    assert (
        result[
            "predictions"
        ][0][
            "predicted_class"
        ]
        == "Normal_Weight"
    )

    mock_get.assert_called_once_with(
        "http://127.0.0.1:5000/predictions",
        timeout=5,
    )


@patch(
    "frontend.services."
    "api_client.requests.get"
)
def test_get_prediction_detail(
    mock_get,
):
    mock_response = Mock()

    mock_response.ok = True
    mock_response.status_code = 200

    mock_response.json.return_value = {
        "id": 7,

        "inputs": {
            "Age": 25.0,
        },

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

        "model_name":
            "Tuned Gradient Boosting",

        "scikit_learn_version":
            "1.8.0",

        "created_at":
            "2026-08-10 12:00:00",
    }

    mock_get.return_value = (
        mock_response
    )

    client = APIClient()

    result = (
        client.get_prediction(
            7
        )
    )

    assert (
        result["id"]
        == 7
    )

    assert (
        result["inputs"]["Age"]
        == 25.0
    )

    assert (
        result["predicted_class"]
        == "Normal_Weight"
    )

    mock_get.assert_called_once_with(
        (
            "http://127.0.0.1:5000/"
            "predictions/7"
        ),
        timeout=5,
    )


@patch(
    "frontend.services."
    "api_client.requests.post"
)
def test_predict_surfaces_backend_error(
    mock_post,
):
    mock_response = Mock()

    mock_response.ok = False
    mock_response.status_code = 400

    mock_response.json.return_value = {
        "error":
            "validation_error",

        "message":
            "Age must be numeric.",
    }

    mock_post.return_value = (
        mock_response
    )

    client = APIClient()

    with pytest.raises(
        APIClientError,
        match="Age must be numeric",
    ) as error_info:

        client.predict(
            {
                "Age":
                    "twenty",
            }
        )

    assert (
        error_info.value.status_code
        == 400
    )


@patch(
    "frontend.services."
    "api_client.requests.get"
)
def test_invalid_json_response(
    mock_get,
):
    mock_response = Mock()

    mock_response.ok = True
    mock_response.status_code = 200

    mock_response.json.side_effect = (
        ValueError(
            "Invalid JSON"
        )
    )

    mock_get.return_value = (
        mock_response
    )

    client = APIClient()

    with pytest.raises(
        APIClientError,
        match="invalid JSON",
    ):
        client.get_health()


@patch(
    "frontend.services."
    "api_client.requests.get"
)
def test_get_prediction_report(
    mock_get,
):
    mock_response = Mock()

    mock_response.ok = True
    mock_response.status_code = 200

    mock_response.content = (
        b"%PDF-1.4 test content"
    )

    mock_get.return_value = (
        mock_response
    )

    client = APIClient()

    result = (
        client.get_prediction_report(
            7
        )
    )

    assert isinstance(
        result,
        bytes,
    )

    assert (
        result.startswith(
            b"%PDF"
        )
    )

    mock_get.assert_called_once_with(
        (
            "http://127.0.0.1:5000/"
            "predictions/7/report"
        ),
        timeout=5,
    )