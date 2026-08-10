import pytest

from frontend.components.prediction_history import (
    build_history_dataframe,
    build_input_dataframe,
)


def test_build_history_dataframe():
    predictions = [
        {
            "id": 2,
            "predicted_class":
                "Normal_Weight",
            "confidence":
                0.875,
            "model_name":
                "Tuned Gradient Boosting",
            "created_at":
                "2026-08-10 12:00:00",
        }
    ]

    result = (
        build_history_dataframe(
            predictions
        )
    )

    assert len(
        result
    ) == 1

    assert (
        result.iloc[0]["ID"]
        == 2
    )

    assert (
        result.iloc[0]["Category"]
        == "Normal Weight"
    )

    assert (
        result.iloc[0]["Confidence"]
        == "87.50%"
    )


def test_build_history_dataframe_empty():
    result = (
        build_history_dataframe(
            []
        )
    )

    assert result.empty


def test_build_input_dataframe():
    inputs = {
        "Age": 25.0,
        "Height": 1.70,
        "Weight": 70.0,
        "Gender": "Male",
    }

    result = (
        build_input_dataframe(
            inputs
        )
    )

    assert len(
        result
    ) == 16

    age_row = result[
        result[
            "Feature"
        ]
        == "Age"
    ].iloc[0]

    assert (
        age_row["Value"]
        == pytest.approx(
            25.0
        )
    )