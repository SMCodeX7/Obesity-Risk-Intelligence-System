from frontend.components.prediction_history import (
    FEATURE_LABELS,
    _extract_probabilities,
    _format_percentage,
    _prepare_result,
    build_history_dataframe,
    build_input_dataframe,
)
from frontend.components.prediction_result import (
    CLASS_ORDER,
    build_probability_dataframe,
    format_class_name,
)


SAMPLE_PROBABILITIES = {
    "Insufficient_Weight": 0.02,
    "Normal_Weight": 0.10,
    "Overweight_Level_I": 0.08,
    "Overweight_Level_II": 0.05,
    "Obesity_Type_I": 0.15,
    "Obesity_Type_II": 0.55,
    "Obesity_Type_III": 0.05,
}


SAMPLE_INPUTS = {
    "Age": 30.0,
    "Height": 1.75,
    "Weight": 82.0,
    "Gender": "Male",
    "family_history_with_overweight": "yes",
    "FCVC": 2.5,
    "NCP": 3.0,
    "CAEC": "Sometimes",
    "FAVC": "yes",
    "CH2O": 2.0,
    "CALC": "no",
    "FAF": 1.5,
    "TUE": 1.0,
    "SMOKE": "no",
    "SCC": "no",
    "MTRANS": "Public_Transportation",
}


def test_format_class_name():
    assert (
        format_class_name(
            "Obesity_Type_II"
        )
        == "Obesity Type II"
    )

    assert (
        format_class_name(
            "Normal_Weight"
        )
        == "Normal Weight"
    )


def test_probability_dataframe_contains_all_classes():
    dataframe = (
        build_probability_dataframe(
            SAMPLE_PROBABILITIES
        )
    )

    assert len(
        dataframe
    ) == 7

    assert set(
        dataframe["Category"]
    ) == {
        format_class_name(
            class_name
        )
        for class_name in CLASS_ORDER
    }


def test_probability_dataframe_is_sorted():
    dataframe = (
        build_probability_dataframe(
            SAMPLE_PROBABILITIES
        )
    )

    assert (
        dataframe.iloc[0][
            "Category"
        ]
        == "Obesity Type II"
    )

    assert (
        dataframe.iloc[0][
            "Probability"
        ]
        == 0.55
    )


def test_probability_dataframe_percentage():
    dataframe = (
        build_probability_dataframe(
            SAMPLE_PROBABILITIES
        )
    )

    obesity_row = dataframe[
        dataframe["Category"]
        == "Obesity Type II"
    ].iloc[0]

    assert (
        abs(
            obesity_row[
                "Probability (%)"
            ]
            - 55.0
        )
        < 1e-9
    )


def test_history_dataframe_formatting():
    predictions = [
        {
            "id": 10,
            "predicted_class":
                "Obesity_Type_II",
            "confidence": 0.9123,
            "model_name":
                "Tuned Gradient Boosting",
            "created_at":
                "2026-08-11T10:30:00",
        }
    ]

    dataframe = (
        build_history_dataframe(
            predictions
        )
    )

    assert len(
        dataframe
    ) == 1

    assert (
        dataframe.iloc[0]["ID"]
        == 10
    )

    assert (
        dataframe.iloc[0][
            "Category"
        ]
        == "Obesity Type II"
    )

    assert (
        dataframe.iloc[0][
            "Confidence"
        ]
        == "91.23%"
    )

    assert (
        dataframe.iloc[0][
            "Model"
        ]
        == "Tuned Gradient Boosting"
    )


def test_input_dataframe_contains_all_features():
    dataframe = (
        build_input_dataframe(
            SAMPLE_INPUTS
        )
    )

    assert len(
        dataframe
    ) == 16

    assert set(
        dataframe["Feature"]
    ) == set(
        FEATURE_LABELS.values()
    )


def test_format_percentage():
    assert (
        _format_percentage(
            0.91234
        )
        == "91.23%"
    )

    assert (
        _format_percentage(
            None
        )
        == "Unavailable"
    )


def test_extract_probabilities_from_dictionary():
    sources = [
        {
            "probabilities":
                SAMPLE_PROBABILITIES
        }
    ]

    result = (
        _extract_probabilities(
            sources
        )
    )

    assert (
        result
        == SAMPLE_PROBABILITIES
    )


def test_extract_probabilities_from_json():
    sources = [
        {
            "probabilities_json":
                """
                {
                    "Insufficient_Weight": 0.02,
                    "Normal_Weight": 0.10,
                    "Overweight_Level_I": 0.08,
                    "Overweight_Level_II": 0.05,
                    "Obesity_Type_I": 0.15,
                    "Obesity_Type_II": 0.55,
                    "Obesity_Type_III": 0.05
                }
                """
        }
    ]

    result = (
        _extract_probabilities(
            sources
        )
    )

    assert (
        result[
            "Obesity_Type_II"
        ]
        == 0.55
    )

    assert len(
        result
    ) == 7


def test_prepare_result_from_nested_result():
    detail = {
        "id": 22,
        "result": {
            "predicted_class":
                "Obesity_Type_II",
            "confidence": 0.91,
            "probabilities":
                SAMPLE_PROBABILITIES,
            "model_name":
                "Tuned Gradient Boosting",
            "scikit_learn_version":
                "1.8.0",
        },
        "created_at":
            "2026-08-11T10:30:00",
    }

    result = (
        _prepare_result(
            detail,
            22,
        )
    )

    assert (
        result[
            "prediction_id"
        ]
        == 22
    )

    assert (
        result[
            "predicted_class"
        ]
        == "Obesity_Type_II"
    )

    assert (
        result[
            "confidence"
        ]
        == 0.91
    )

    assert (
        result[
            "probabilities"
        ]
        == SAMPLE_PROBABILITIES
    )


def test_prepare_result_from_top_level_fields():
    detail = {
        "id": 23,
        "predicted_class":
            "Normal_Weight",
        "confidence": 0.88,
        "probabilities":
            SAMPLE_PROBABILITIES,
        "model_name":
            "Tuned Gradient Boosting",
        "scikit_learn_version":
            "1.8.0",
        "created_at":
            "2026-08-11T11:00:00",
    }

    result = (
        _prepare_result(
            detail,
            23,
        )
    )

    assert (
        result[
            "prediction_id"
        ]
        == 23
    )

    assert (
        result[
            "predicted_class"
        ]
        == "Normal_Weight"
    )

    assert (
        result[
            "confidence"
        ]
        == 0.88
    )

    assert (
        result[
            "model_name"
        ]
        == "Tuned Gradient Boosting"
    )


def test_prepare_result_from_probabilities_json():
    detail = {
        "id": 24,
        "predicted_class":
            "Obesity_Type_I",
        "confidence": 0.84,
        "probabilities_json":
            """
            {
                "Insufficient_Weight": 0.01,
                "Normal_Weight": 0.03,
                "Overweight_Level_I": 0.04,
                "Overweight_Level_II": 0.06,
                "Obesity_Type_I": 0.84,
                "Obesity_Type_II": 0.01,
                "Obesity_Type_III": 0.01
            }
            """,
    }

    result = (
        _prepare_result(
            detail,
            24,
        )
    )

    assert (
        result[
            "prediction_id"
        ]
        == 24
    )

    assert (
        result[
            "predicted_class"
        ]
        == "Obesity_Type_I"
    )

    assert (
        result[
            "probabilities"
        ][
            "Obesity_Type_I"
        ]
        == 0.84
    )

    assert len(
        result[
            "probabilities"
        ]
    ) == 7