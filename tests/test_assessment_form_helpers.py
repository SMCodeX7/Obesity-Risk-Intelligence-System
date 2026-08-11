from frontend.components.assessment_form import (
    DEFAULT_ASSESSMENT_DATA,
    _option_index,
    build_assessment_payload,
)


EXPECTED_FEATURES = {
    "Age",
    "Height",
    "Weight",
    "FCVC",
    "NCP",
    "CH2O",
    "FAF",
    "TUE",
    "CAEC",
    "CALC",
    "Gender",
    "family_history_with_overweight",
    "FAVC",
    "SMOKE",
    "SCC",
    "MTRANS",
}


SAMPLE_ASSESSMENT_DATA = {
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


def test_assessment_payload_has_exact_features():
    payload = build_assessment_payload(
        SAMPLE_ASSESSMENT_DATA
    )

    assert (
        set(payload.keys())
        == EXPECTED_FEATURES
    )

    assert len(payload) == 16


def test_assessment_payload_preserves_values():
    payload = build_assessment_payload(
        SAMPLE_ASSESSMENT_DATA
    )

    assert payload["Age"] == 25.0
    assert payload["Height"] == 1.70
    assert payload["Weight"] == 70.0

    assert payload["FCVC"] == 2.0
    assert payload["NCP"] == 3.0
    assert payload["CH2O"] == 2.0
    assert payload["FAF"] == 1.0
    assert payload["TUE"] == 1.0

    assert (
        payload["CAEC"]
        == "Sometimes"
    )

    assert (
        payload["CALC"]
        == "no"
    )

    assert (
        payload["Gender"]
        == "Male"
    )

    assert (
        payload[
            "family_history_with_overweight"
        ]
        == "yes"
    )

    assert (
        payload["FAVC"]
        == "yes"
    )

    assert (
        payload["SMOKE"]
        == "no"
    )

    assert (
        payload["SCC"]
        == "no"
    )

    assert (
        payload["MTRANS"]
        == "Public_Transportation"
    )


def test_assessment_numeric_values_are_floats():
    assessment_data = (
        SAMPLE_ASSESSMENT_DATA.copy()
    )

    assessment_data["Age"] = 30
    assessment_data["Weight"] = 80

    payload = build_assessment_payload(
        assessment_data
    )

    numerical_features = [
        "Age",
        "Height",
        "Weight",
        "FCVC",
        "NCP",
        "CH2O",
        "FAF",
        "TUE",
    ]

    for feature in numerical_features:
        assert isinstance(
            payload[feature],
            float,
        )


def test_default_assessment_data_is_complete():
    assert (
        set(
            DEFAULT_ASSESSMENT_DATA.keys()
        )
        == EXPECTED_FEATURES
    )

    assert (
        len(
            DEFAULT_ASSESSMENT_DATA
        )
        == 16
    )


def test_option_index_returns_matching_position():
    options = [
        "no",
        "Sometimes",
        "Frequently",
        "Always",
    ]

    assert (
        _option_index(
            options,
            "Frequently",
        )
        == 2
    )


def test_option_index_falls_back_to_first_option():
    options = [
        "Female",
        "Male",
    ]

    assert (
        _option_index(
            options,
            "Unknown",
        )
        == 0
    )