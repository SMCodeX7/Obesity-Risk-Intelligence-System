from backend import (
    create_app,
)


def test_model_info_endpoint():
    app = create_app(
        {
            "TESTING": True,
        }
    )

    client = (
        app.test_client()
    )

    response = client.get(
        "/model-info"
    )

    assert (
        response.status_code
        == 200
    )

    data = (
        response.get_json()
    )

    assert (
        data["model_loaded"]
        is True
    )

    assert (
        data["selected_model"]
        == "Tuned Gradient Boosting"
    )

    assert (
        data[
            "predictive_feature_count"
        ]
        == 16
    )

    assert (
        data[
            "transformed_feature_count"
        ]
        == 25
    )

    assert (
        data[
            "target_class_count"
        ]
        == 7
    )

    assert (
        data[
            "scikit_learn_version"
        ]
        == "1.8.0"
    )