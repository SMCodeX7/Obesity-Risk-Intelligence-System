from backend import (
    create_app,
)
from backend.database import (
    init_db,
)


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


def create_history_test_app(
    tmp_path,
):
    database_path = (
        tmp_path
        / "history_test.db"
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


def test_prediction_is_saved(
    tmp_path,
):
    app = create_history_test_app(
        tmp_path
    )

    client = (
        app.test_client()
    )

    response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    assert (
        response.status_code
        == 200
    )

    data = (
        response.get_json()
    )

    assert (
        data["prediction_id"]
        >= 1
    )

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
        == 1
    )

    assert (
        len(
            history_data[
                "predictions"
            ]
        )
        == 1
    )

    assert (
        history_data[
            "predictions"
        ][0]["id"]
        == data[
            "prediction_id"
        ]
    )


def test_get_prediction_detail(
    tmp_path,
):
    app = create_history_test_app(
        tmp_path
    )

    client = (
        app.test_client()
    )

    prediction_response = (
        client.post(
            "/predict",
            json=VALID_PAYLOAD,
        )
    )

    prediction_data = (
        prediction_response.get_json()
    )

    prediction_id = (
        prediction_data[
            "prediction_id"
        ]
    )

    response = client.get(
        f"/predictions/"
        f"{prediction_id}"
    )

    assert (
        response.status_code
        == 200
    )

    data = (
        response.get_json()
    )

    assert (
        data["id"]
        == prediction_id
    )

    assert (
        data["inputs"]["Age"]
        == 25.0
    )

    assert (
        data["inputs"]["Height"]
        == 1.70
    )

    assert (
        data["inputs"]["Weight"]
        == 70.0
    )

    assert (
        data["predicted_class"]
        == prediction_data[
            "predicted_class"
        ]
    )

    assert (
        data["confidence"]
        == prediction_data[
            "confidence"
        ]
    )

    assert (
        len(
            data[
                "probabilities"
            ]
        )
        == 7
    )


def test_prediction_not_found(
    tmp_path,
):
    app = create_history_test_app(
        tmp_path
    )

    client = (
        app.test_client()
    )

    response = client.get(
        "/predictions/999999"
    )

    assert (
        response.status_code
        == 404
    )

    data = (
        response.get_json()
    )

    assert (
        data["error"]
        == "prediction_not_found"
    )