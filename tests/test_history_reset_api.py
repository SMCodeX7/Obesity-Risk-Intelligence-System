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


def create_history_reset_test_app(
    tmp_path,
):
    database_path = (
        tmp_path
        / "history_reset_test.db"
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


def test_history_reset_disabled_by_default(
    tmp_path,
    monkeypatch,
):
    monkeypatch.delenv(
        "OBESITY_ENABLE_HISTORY_RESET",
        raising=False,
    )

    app = (
        create_history_reset_test_app(
            tmp_path
        )
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

    assert (
        prediction_response.status_code
        == 200
    )

    response = client.delete(
        "/predictions"
    )

    assert (
        response.status_code
        == 403
    )

    data = (
        response.get_json()
    )

    assert (
        data["error"]
        == "history_reset_disabled"
    )

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


def test_history_reset_when_enabled(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setenv(
        "OBESITY_ENABLE_HISTORY_RESET",
        "true",
    )

    app = (
        create_history_reset_test_app(
            tmp_path
        )
    )

    client = (
        app.test_client()
    )

    first_response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    second_response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    assert (
        first_response.status_code
        == 200
    )

    assert (
        second_response.status_code
        == 200
    )

    history_before = client.get(
        "/predictions"
    )

    history_before_data = (
        history_before.get_json()
    )

    assert (
        history_before_data["count"]
        == 2
    )

    response = client.delete(
        "/predictions"
    )

    assert (
        response.status_code
        == 200
    )

    data = (
        response.get_json()
    )

    assert (
        data["message"]
        == "Prediction history cleared."
    )

    assert (
        data["deleted_count"]
        == 2
    )

    history_after = client.get(
        "/predictions"
    )

    history_after_data = (
        history_after.get_json()
    )

    assert (
        history_after_data["count"]
        == 0
    )

    assert (
        history_after_data[
            "predictions"
        ]
        == []
    )


def test_history_reset_keeps_id_sequence(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setenv(
        "OBESITY_ENABLE_HISTORY_RESET",
        "true",
    )

    app = (
        create_history_reset_test_app(
            tmp_path
        )
    )

    client = (
        app.test_client()
    )

    first_response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    first_data = (
        first_response.get_json()
    )

    first_id = (
        first_data[
            "prediction_id"
        ]
    )

    clear_response = client.delete(
        "/predictions"
    )

    assert (
        clear_response.status_code
        == 200
    )

    second_response = client.post(
        "/predict",
        json=VALID_PAYLOAD,
    )

    second_data = (
        second_response.get_json()
    )

    second_id = (
        second_data[
            "prediction_id"
        ]
    )

    assert (
        second_id
        > first_id
    )