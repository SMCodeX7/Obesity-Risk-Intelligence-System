from backend import create_app
from backend.database import init_db


VALID_PAYLOAD = {
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


def create_integration_app(
    tmp_path,
):
    database_path = (
        tmp_path
        / "integration.db"
    )

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(
                database_path
            ),
        }
    )

    with app.app_context():
        init_db()

    return app


def test_complete_prediction_workflow(
    tmp_path,
):
    app = create_integration_app(
        tmp_path
    )

    client = app.test_client()

    # 1. API should be healthy
    health_response = client.get(
        "/health"
    )

    assert (
        health_response.status_code
        == 200
    )

    assert (
        health_response
        .get_json()["status"]
        == "ok"
    )

    # 2. Model information
    model_response = client.get(
        "/model-info"
    )

    assert (
        model_response.status_code
        == 200
    )

    model_data = (
        model_response.get_json()
    )

    assert (
        model_data["model_loaded"]
        is True
    )

    # 3. History should begin empty
    history_response = client.get(
        "/predictions"
    )

    assert (
        history_response.status_code
        == 200
    )

    history_data = (
        history_response.get_json()
    )

    assert (
        history_data["count"]
        == 0
    )

    # 4. Create prediction
    prediction_response = (
        client.post(
            "/predict",
            json=VALID_PAYLOAD,
        )
    )

    assert (
        prediction_response.status_code
        == 200
    )

    prediction_data = (
        prediction_response.get_json()
    )

    assert (
        "prediction_id"
        in prediction_data
    )

    assert (
        "predicted_class"
        in prediction_data
    )

    assert (
        "confidence"
        in prediction_data
    )

    assert (
        "probabilities"
        in prediction_data
    )

    prediction_id = (
        prediction_data[
            "prediction_id"
        ]
    )

    assert (
        prediction_id >= 1
    )

    assert (
        0.0
        <= prediction_data[
            "confidence"
        ]
        <= 1.0
    )

    assert (
        len(
            prediction_data[
                "probabilities"
            ]
        )
        == 7
    )

    probability_sum = sum(
        prediction_data[
            "probabilities"
        ].values()
    )

    assert (
        abs(
            probability_sum
            - 1.0
        )
        < 1e-8
    )

    # 5. Prediction should now
    # appear in history
    history_response = client.get(
        "/predictions"
    )

    history_data = (
        history_response.get_json()
    )

    assert (
        history_data["count"]
        == 1
    )

    assert (
        history_data[
            "predictions"
        ][0]["id"]
        == prediction_id
    )

    # 6. Retrieve full saved record
    detail_response = client.get(
        f"/predictions/"
        f"{prediction_id}"
    )

    assert (
        detail_response.status_code
        == 200
    )

    detail_data = (
        detail_response.get_json()
    )

    assert (
        detail_data["id"]
        == prediction_id
    )

    assert (
        detail_data[
            "inputs"
        ]["Age"]
        == 25.0
    )

    assert (
        detail_data[
            "inputs"
        ]["Height"]
        == 1.70
    )

    assert (
        detail_data[
            "inputs"
        ]["Weight"]
        == 70.0
    )

    assert (
        detail_data[
            "predicted_class"
        ]
        == prediction_data[
            "predicted_class"
        ]
    )

    assert (
        detail_data[
            "confidence"
        ]
        == prediction_data[
            "confidence"
        ]
    )

    # 7. PDF should be available
    report_response = client.get(
        f"/predictions/"
        f"{prediction_id}/report"
    )

    assert (
        report_response.status_code
        == 200
    )

    assert (
        report_response.mimetype
        == "application/pdf"
    )

    assert (
        report_response.data.startswith(
            b"%PDF"
        )
    )


def test_multiple_predictions_are_saved(
    tmp_path,
):
    app = create_integration_app(
        tmp_path
    )

    client = app.test_client()

    first_response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    second_payload = (
        VALID_PAYLOAD.copy()
    )

    second_payload[
        "Weight"
    ] = 80.0

    second_response = client.post(
        "/predict",
        json=second_payload,
    )

    assert (
        first_response.status_code
        == 200
    )

    assert (
        second_response.status_code
        == 200
    )

    first_id = (
        first_response
        .get_json()[
            "prediction_id"
        ]
    )

    second_id = (
        second_response
        .get_json()[
            "prediction_id"
        ]
    )

    assert (
        second_id
        > first_id
    )

    history_response = client.get(
        "/predictions"
    )

    history_data = (
        history_response.get_json()
    )

    assert (
        history_data["count"]
        == 2
    )

    assert (
        history_data[
            "predictions"
        ][0]["id"]
        == second_id
    )

    assert (
        history_data[
            "predictions"
        ][1]["id"]
        == first_id
    )