import pandas as pd
import streamlit as st

from frontend.components.prediction_result import (
    format_class_name,
    render_prediction_result,
)
from frontend.components.report_download import (
    render_pdf_download,
)
from frontend.services.api_client import (
    APIClientError,
)


FEATURE_LABELS = {
    "Age":
        "Age",

    "Height":
        "Height (m)",

    "Weight":
        "Weight (kg)",

    "FCVC":
        "Vegetable Consumption",

    "NCP":
        "Main Meals",

    "CH2O":
        "Water Consumption",

    "FAF":
        "Physical Activity",

    "TUE":
        "Technology Use",

    "CAEC":
        "Food Between Meals",

    "CALC":
        "Alcohol Consumption",

    "Gender":
        "Gender",

    "family_history_with_overweight":
        "Family History",

    "FAVC":
        "High-Calorie Food",

    "SMOKE":
        "Smoking",

    "SCC":
        "Calorie Monitoring",

    "MTRANS":
        "Transportation",
}


def build_history_dataframe(
    predictions,
):
    rows = []

    for prediction in predictions:
        confidence = float(
            prediction.get(
                "confidence",
                0.0,
            )
        )

        rows.append(
            {
                "ID":
                    prediction.get(
                        "id"
                    ),

                "Category":
                    format_class_name(
                        prediction.get(
                            "predicted_class",
                            "Unknown",
                        )
                    ),

                "Confidence":
                    f"{confidence * 100:.2f}%",

                "Model":
                    prediction.get(
                        "model_name",
                        "Unknown",
                    ),

                "Created At":
                    prediction.get(
                        "created_at",
                        "Unknown",
                    ),
            }
        )

    return pd.DataFrame(
        rows
    )


def build_input_dataframe(
    inputs,
):
    rows = []

    for feature, label in (
        FEATURE_LABELS.items()
    ):
        rows.append(
            {
                "Feature":
                    label,

                "Value":
                    inputs.get(
                        feature,
                        "Unavailable",
                    ),
            }
        )

    return pd.DataFrame(
        rows
    )


def render_prediction_history(
    api_client,
):
    st.subheader(
        "Prediction History"
    )

    st.write(
        "Review previously saved "
        "obesity-risk assessments."
    )

    try:
        history_data = (
            api_client
            .get_predictions()
        )

    except APIClientError as error:
        st.error(
            "Unable to load "
            "prediction history."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(
                str(error)
            )

        return

    predictions = (
        history_data.get(
            "predictions",
            [],
        )
    )

    if not predictions:
        st.info(
            "No saved assessments "
            "are available yet."
        )

        st.write(
            "Create an assessment "
            "first and it will appear "
            "here automatically."
        )

        return

    history_df = (
        build_history_dataframe(
            predictions
        )
    )

    total_predictions = (
        len(
            predictions
        )
    )

    st.metric(
        "Saved Assessments",
        total_predictions,
        border=True,
    )

    st.markdown(
        "### Recent Assessments"
    )

    st.dataframe(
        history_df,
        width="stretch",
        hide_index=True,
    )

    st.markdown(
        "### Open Saved Assessment"
    )

    prediction_ids = [
        prediction["id"]
        for prediction
        in predictions
    ]

    selected_prediction_id = (
        st.selectbox(
            "Select assessment",
            options=prediction_ids,
            format_func=lambda value:
                f"Assessment #{value}",
            key=(
                "history_prediction_selector"
            ),
        )
    )

    if st.button(
        "View Assessment",
        type="primary",
        key="view_history_prediction",
    ):
        st.session_state[
            "selected_history_prediction_id"
        ] = selected_prediction_id

    selected_history_id = (
        st.session_state.get(
            "selected_history_prediction_id"
        )
    )

    if selected_history_id is None:
        return

    try:
        prediction_detail = (
            api_client.get_prediction(
                selected_history_id
            )
        )

    except APIClientError as error:
        st.error(
            "Unable to load the "
            "selected assessment."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(
                str(error)
            )

        return

    st.divider()

    st.subheader(
        f"Assessment "
        f"#{prediction_detail['id']}"
    )

    col1, col2 = (
        st.columns(2)
    )

    with col1:
        st.write(
            "**Created:**"
        )

        st.write(
            prediction_detail.get(
                "created_at",
                "Unavailable",
            )
        )

    with col2:
        st.write(
            "**Model:**"
        )

        st.write(
            prediction_detail.get(
                "model_name",
                "Unavailable",
            )
        )

    st.markdown(
        "### Assessment Inputs"
    )

    input_df = (
        build_input_dataframe(
            prediction_detail.get(
                "inputs",
                {},
            )
        )
    )

    st.dataframe(
        input_df,
        width="stretch",
        hide_index=True,
    )

    render_prediction_result(
        prediction_detail
    )

    st.markdown(
        "### Assessment Report"
    )

    st.write(
        "Download a PDF copy of "
        "this saved assessment."
    )

    render_pdf_download(
        api_client=api_client,
        prediction_id=(
            prediction_detail[
                "id"
            ]
        ),
        key_prefix="history",
    )