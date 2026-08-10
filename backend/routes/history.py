from flask import Blueprint

from backend.repositories.prediction_repository import (
    get_prediction,
    list_predictions,
)


history_bp = Blueprint(
    "history",
    __name__,
)


@history_bp.get(
    "/predictions"
)
def prediction_history():
    predictions = (
        list_predictions()
    )

    return {
        "count":
            len(
                predictions
            ),

        "predictions":
            predictions,
    }, 200


@history_bp.get(
    "/predictions/<int:prediction_id>"
)
def prediction_detail(
    prediction_id,
):
    prediction = (
        get_prediction(
            prediction_id
        )
    )

    if prediction is None:
        return {
            "error":
                "prediction_not_found",

            "message":
                "Prediction record "
                "not found.",
        }, 404

    return prediction, 200