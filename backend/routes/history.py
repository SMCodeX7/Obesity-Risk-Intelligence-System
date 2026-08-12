import os
from io import BytesIO

from flask import (
    Blueprint,
    send_file,
)

from backend.repositories.prediction_repository import (
    clear_predictions,
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


def is_history_reset_enabled():
    value = os.getenv(
        "OBESITY_ENABLE_HISTORY_RESET",
        "false",
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


def is_history_access_enabled():
    value = os.getenv(
        "OBESITY_ENABLE_HISTORY_ACCESS",
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


def history_disabled_response():
    return {
        "error":
            "history_access_disabled",

        "message":
            (
                "Prediction history is "
                "disabled for this deployment."
            ),
    }, 403


@history_bp.get(
    "/predictions"
)
def prediction_history():
    if not is_history_access_enabled():
        return history_disabled_response()

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


@history_bp.delete(
    "/predictions"
)
def clear_prediction_history():
    if not is_history_access_enabled():
        return history_disabled_response()

    if not is_history_reset_enabled():
        return {
            "error":
                "history_reset_disabled",

            "message":
                "Prediction history reset "
                "is disabled.",
        }, 403

    deleted_count = (
        clear_predictions()
    )

    return {
        "message":
            "Prediction history cleared.",

        "deleted_count":
            deleted_count,
    }, 200


@history_bp.get(
    "/predictions/<int:prediction_id>"
)
def prediction_detail(
    prediction_id,
):
    if not is_history_access_enabled():
        return history_disabled_response()

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
    if not is_history_access_enabled():
        return history_disabled_response()

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
            "obesity-risk-assessment-report.pdf"
        ),
    )