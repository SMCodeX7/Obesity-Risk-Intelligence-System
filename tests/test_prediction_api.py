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


def create_database_app(
    tmp_path,
):
    database_path = (
        tmp_path
        / "prediction_test.db"
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


def test_prediction_endpoint(
    tmp_path,
):
    app = create_database_app(
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
        "prediction_id"
        in data
    )

    assert (
        data["prediction_id"]
        >= 1
    )

    assert (
        "predicted_class"
        in data
    )

    assert (
        "confidence"
        in data
    )

    assert (
        "probabilities"
        in data
    )

    model_service = (
        app.extensions[
            "obesity_risk_model"
        ]
    )

    target_classes = (
        model_service.metadata[
            "target_classes"
        ]
    )

    assert (
        data["predicted_class"]
        in target_classes
    )

    assert (
        0.0
        <= data["confidence"]
        <= 1.0
    )

    assert (
        set(
            data[
                "probabilities"
            ]
        )
        == set(
            target_classes
        )
    )

    probability_sum = sum(
        data[
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


def test_prediction_rejects_missing_features(
    tmp_path,
):
    app = create_database_app(
        tmp_path
    )

    client = (
        app.test_client()
    )

    response = client.post(
        "/predict",
        json={
            "Age": 25.0
        },
    )

    assert (
        response.status_code
        == 400
    )

    data = (
        response.get_json()
    )

    assert (
        data["error"]
        == "validation_error"
    )

    assert (
        "Missing required features"
        in data["message"]
    )