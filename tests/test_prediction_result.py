import pytest

from frontend.components.prediction_result import (
    build_probability_dataframe,
    format_class_name,
)


def test_format_class_name():
    assert (
        format_class_name(
            "Normal_Weight"
        )
        == "Normal Weight"
    )

    assert (
        format_class_name(
            "Overweight_Level_I"
        )
        == "Overweight Level I"
    )

    assert (
        format_class_name(
            "Obesity_Type_III"
        )
        == "Obesity Type III"
    )


def test_build_probability_dataframe():
    probabilities = {
        "Insufficient_Weight":
            0.05,

        "Normal_Weight":
            0.70,

        "Overweight_Level_I":
            0.10,

        "Overweight_Level_II":
            0.06,

        "Obesity_Type_I":
            0.04,

        "Obesity_Type_II":
            0.03,

        "Obesity_Type_III":
            0.02,
    }

    result = (
        build_probability_dataframe(
            probabilities
        )
    )

    assert len(
        result
    ) == 7

    assert list(
        result.columns
    ) == [
        "Category",
        "Probability",
        "Probability (%)",
    ]

    assert (
        result.iloc[0][
            "Category"
        ]
        == "Normal Weight"
    )

    assert (
        result.iloc[0][
            "Probability"
        ]
        == pytest.approx(
            0.70
        )
    )

    assert (
        result.iloc[0][
            "Probability (%)"
        ]
        == pytest.approx(
            70.0
        )
    )

    assert (
        result[
            "Probability"
        ].sum()
        == pytest.approx(
            1.0
        )
    )


def test_probability_dataframe_is_sorted():
    probabilities = {
        "Insufficient_Weight":
            0.10,

        "Normal_Weight":
            0.20,

        "Overweight_Level_I":
            0.30,

        "Overweight_Level_II":
            0.15,

        "Obesity_Type_I":
            0.10,

        "Obesity_Type_II":
            0.10,

        "Obesity_Type_III":
            0.05,
    }

    result = (
        build_probability_dataframe(
            probabilities
        )
    )

    probability_values = list(
        result[
            "Probability"
        ]
    )

    assert probability_values == (
        sorted(
            probability_values,
            reverse=True,
        )
    )