from flask import (
    Blueprint,
    current_app,
)


model_info_bp = Blueprint(
    "model_info",
    __name__,
)


@model_info_bp.get(
    "/model-info"
)
def model_info():
    model_service = (
        current_app
        .extensions[
            "obesity_risk_model"
        ]
    )

    return (
        model_service
        .get_model_info()
    ), 200