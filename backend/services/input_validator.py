import math

from src.preprocessing import (
    PREDICTIVE_FEATURES,
)


NUMERIC_RANGES = {
    "Age": (1.0, 120.0),
    "Height": (0.5, 2.5),
    "Weight": (10.0, 350.0),
    "FCVC": (1.0, 3.0),
    "NCP": (1.0, 4.0),
    "CH2O": (1.0, 3.0),
    "FAF": (0.0, 3.0),
    "TUE": (0.0, 2.0),
}


CATEGORY_CHOICES = {
    "CAEC": {
        "no",
        "Sometimes",
        "Frequently",
        "Always",
    },

    "CALC": {
        "no",
        "Sometimes",
        "Frequently",
    },

    "Gender": {
        "Female",
        "Male",
    },

    "family_history_with_overweight": {
        "yes",
        "no",
    },

    "FAVC": {
        "yes",
        "no",
    },

    "SMOKE": {
        "yes",
        "no",
    },

    "SCC": {
        "yes",
        "no",
    },

    "MTRANS": {
        "Automobile",
        "Bike",
        "Motorbike",
        "Public_Transportation",
        "Walking",
    },
}


def validate_prediction_payload(
    payload,
):
    if not isinstance(
        payload,
        dict,
    ):
        raise ValueError(
            "Request body must be a JSON object."
        )

    required_features = set(
        PREDICTIVE_FEATURES
    )

    supplied_features = set(
        payload.keys()
    )

    missing_features = (
        required_features
        - supplied_features
    )

    if missing_features:
        raise ValueError(
            "Missing required features: "
            + ", ".join(
                sorted(
                    missing_features
                )
            )
        )

    unexpected_features = (
        supplied_features
        - required_features
    )

    if unexpected_features:
        raise ValueError(
            "Unexpected features: "
            + ", ".join(
                sorted(
                    unexpected_features
                )
            )
        )

    validated = {}

    for feature in (
        PREDICTIVE_FEATURES
    ):

        value = payload[
            feature
        ]

        if feature in NUMERIC_RANGES:

            if (
                isinstance(value, bool)
                or not isinstance(
                    value,
                    (int, float),
                )
            ):
                raise ValueError(
                    f"{feature} must be numeric."
                )

            numeric_value = float(
                value
            )

            if not math.isfinite(
                numeric_value
            ):
                raise ValueError(
                    f"{feature} must be finite."
                )

            minimum, maximum = (
                NUMERIC_RANGES[
                    feature
                ]
            )

            if not (
                minimum
                <= numeric_value
                <= maximum
            ):
                raise ValueError(
                    f"{feature} must be between "
                    f"{minimum} and {maximum}."
                )

            validated[
                feature
            ] = numeric_value

        else:

            if not isinstance(
                value,
                str,
            ):
                raise ValueError(
                    f"{feature} must be a string."
                )

            if (
                value
                not in CATEGORY_CHOICES[
                    feature
                ]
            ):
                allowed_values = (
                    ", ".join(
                        sorted(
                            CATEGORY_CHOICES[
                                feature
                            ]
                        )
                    )
                )

                raise ValueError(
                    f"Invalid value for "
                    f"{feature}. "
                    f"Allowed values: "
                    f"{allowed_values}."
                )

            validated[
                feature
            ] = value

    return validated