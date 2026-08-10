from io import BytesIO

from flask import (
    Blueprint,
    send_file,
)

from backend.repositories.prediction_repository import (
    get_prediction,
    list_predictions,
)
from backend.services.pdf_report_service import (
    generate_prediction_report,
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


@history_bp.get(
    "/predictions/"
    "<int:prediction_id>/report"
)
def prediction_report(
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

    pdf_bytes = (
        generate_prediction_report(
            prediction
        )
    )

    pdf_stream = BytesIO(
        pdf_bytes
    )

    pdf_stream.seek(0)

    return send_file(
        pdf_stream,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=(
            "obesity-risk-"
            f"assessment-{prediction_id}.pdf"
        ),
    )