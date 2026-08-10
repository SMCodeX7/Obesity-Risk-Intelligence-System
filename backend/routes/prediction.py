from flask import (
    Blueprint,
    current_app,
    request,
)

from backend.services.input_validator import (
    validate_prediction_payload,
)


prediction_bp = Blueprint(
    "prediction",
    __name__,
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
        current_app
        .extensions[
            "obesity_risk_model"
        ]
    )

    result = (
        model_service.predict(
            validated_features
        )
    )

    return result, 200