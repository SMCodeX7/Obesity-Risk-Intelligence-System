import os

from flask import (
    Blueprint,
    current_app,
    request,
)

from backend.repositories.prediction_repository import (
    save_prediction,
)
from backend.services.input_validator import (
    validate_prediction_payload,
)


prediction_bp = Blueprint(
    "prediction",
    __name__,
)


def is_prediction_persistence_enabled():
    value = os.getenv(
        "OBESITY_SAVE_PREDICTIONS",
        "true",
    )

    return (
        value.strip().lower()
        in {
            "1",
            "true",
            "yes",
            "on",
        }
    )


@prediction_bp.post(
    "/predict"
)
def predict():
    payload = request.get_json(
        silent=True
    )

    validated_features = (
        validate_prediction_payload(
            payload
        )
    )

    model_service = (
        current_app.extensions[
            "obesity_risk_model"
        ]
    )

    result = (
        model_service.predict(
            validated_features
        )
    )

    if (
        is_prediction_persistence_enabled()
    ):
        prediction_id = (
            save_prediction(
                features=(
                    validated_features
                ),
                prediction_result=(
                    result
                ),
                model_metadata=(
                    model_service.metadata
                ),
            )
        )

        result[
            "prediction_id"
        ] = prediction_id

    return result, 200