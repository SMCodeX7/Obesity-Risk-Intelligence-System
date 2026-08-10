from backend import (
    create_app,
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
    "family_history_with_overweight": "yes",
    "FAVC": "yes",
    "SMOKE": "no",
    "SCC": "no",
    "MTRANS": "Public_Transportation",
}


def create_test_client():
    app = create_app(
        {
            "TESTING": True,
        }
    )

    return app.test_client()


def test_unknown_endpoint_returns_json_404():
    client = (
        create_test_client()
    )

    response = client.get(
        "/does-not-exist"
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
        == "not_found"
    )


def test_predict_rejects_get_method():
    client = (
        create_test_client()
    )

    response = client.get(
        "/predict"
    )

    assert (
        response.status_code
        == 405
    )

    data = (
        response.get_json()
    )

    assert (
        data["error"]
        == "method_not_allowed"
    )


def test_predict_rejects_non_json_body():
    client = (
        create_test_client()
    )

    response = client.post(
        "/predict",
        data="not json",
        content_type="text/plain",
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


def test_predict_rejects_invalid_numeric_type():
    client = (
        create_test_client()
    )

    payload = (
        VALID_PAYLOAD.copy()
    )

    payload["Age"] = "twenty"

    response = client.post(
        "/predict",
        json=payload,
    )

    assert (
        response.status_code
        == 400
    )

    data = (
        response.get_json()
    )

    assert (
        "Age must be numeric"
        in data["message"]
    )


def test_predict_rejects_out_of_range_value():
    client = (
        create_test_client()
    )

    payload = (
        VALID_PAYLOAD.copy()
    )

    payload["Weight"] = -10

    response = client.post(
        "/predict",
        json=payload,
    )

    assert (
        response.status_code
        == 400
    )

    data = (
        response.get_json()
    )

    assert (
        "Weight must be between"
        in data["message"]
    )


def test_predict_rejects_invalid_category():
    client = (
        create_test_client()
    )

    payload = (
        VALID_PAYLOAD.copy()
    )

    payload[
        "Gender"
    ] = "Unknown"

    response = client.post(
        "/predict",
        json=payload,
    )

    assert (
        response.status_code
        == 400
    )

    data = (
        response.get_json()
    )

    assert (
        "Invalid value for Gender"
        in data["message"]
    )


def test_predict_rejects_unexpected_feature():
    client = (
        create_test_client()
    )

    payload = (
        VALID_PAYLOAD.copy()
    )

    payload[
        "ExtraFeature"
    ] = 123

    response = client.post(
        "/predict",
        json=payload,
    )

    assert (
        response.status_code
        == 400
    )

    data = (
        response.get_json()
    )

    assert (
        "Unexpected features"
        in data["message"]
    )