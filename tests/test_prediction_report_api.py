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


def create_report_test_app(
    tmp_path,
):
    database_path = (
        tmp_path
        / "report_test.db"
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


def test_prediction_report_endpoint(
    tmp_path,
):
    app = create_report_test_app(
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

    assert (
        prediction_response.status_code
        == 200
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
        f"/report"
    )

    assert (
        response.status_code
        == 200
    )

    assert (
        response.mimetype
        == "application/pdf"
    )

    assert (
        response.data.startswith(
            b"%PDF"
        )
    )

    content_disposition = (
        response.headers.get(
            "Content-Disposition",
            "",
        )
    )

    assert (
        "attachment"
        in content_disposition
    )

    assert (
        f"assessment-{prediction_id}.pdf"
        in content_disposition
    )


def test_unknown_prediction_report(
    tmp_path,
):
    app = create_report_test_app(
        tmp_path
    )

    client = (
        app.test_client()
    )

    response = client.get(
        "/predictions/"
        "999999/report"
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