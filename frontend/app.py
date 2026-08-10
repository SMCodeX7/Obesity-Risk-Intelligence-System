import streamlit as st

from frontend.components.assessment_form import (
    render_assessment_form,
    reset_assessment_form,
)
from frontend.components.prediction_history import (
    render_prediction_history,
)
from frontend.components.prediction_result import (
    render_prediction_result,
)
from frontend.components.report_download import (
    render_pdf_download,
)
from frontend.services.api_client import (
    APIClient,
    APIClientError,
)


st.set_page_config(
    page_title=(
        "Obesity Risk "
        "Intelligence System"
    ),
    page_icon="📊",
    layout="wide",
)


api_client = APIClient()


if (
    "prediction_result"
    not in st.session_state
):
    st.session_state[
        "prediction_result"
    ] = None


if (
    "selected_history_prediction_id"
    not in st.session_state
):
    st.session_state[
        "selected_history_prediction_id"
    ] = None


st.title(
    "Obesity Risk "
    "Intelligence System"
)

st.caption(
    "Machine Learning-Based "
    "Obesity Risk Assessment"
)


try:
    health_data = (
        api_client.get_health()
    )

    model_info = (
        api_client.get_model_info()
    )

except APIClientError as error:
    st.error(
        "Backend API is unavailable."
    )

    st.write(
        "The Streamlit interface "
        "could not connect to the "
        "Flask API."
    )

    st.info(
        "Start the Flask backend "
        "and refresh this page."
    )

    with st.expander(
        "Technical details"
    ):
        st.code(
            str(error)
        )

    st.stop()


with st.sidebar:
    st.header(
        "Navigation"
    )

    page = st.radio(
        "Application navigation",
        options=[
            "New Assessment",
            "Prediction History",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.header(
        "System Information"
    )

    if (
        health_data.get(
            "status"
        )
        == "ok"
    ):
        st.success(
            "API Connected"
        )

    st.write(
        "**Model:**"
    )

    st.write(
        model_info.get(
            "selected_model",
            "Unknown",
        )
    )

    accuracy = (
        model_info
        .get(
            "final_test_metrics",
            {},
        )
        .get(
            "accuracy"
        )
    )

    macro_f1 = (
        model_info
        .get(
            "final_test_metrics",
            {},
        )
        .get(
            "macro_f1"
        )
    )

    if accuracy is not None:
        st.metric(
            "Test Accuracy",
            f"{accuracy * 100:.2f}%",
        )

    if macro_f1 is not None:
        st.metric(
            "Macro F1",
            f"{macro_f1:.4f}",
        )

    st.divider()

    st.write(
        "**Model Inputs:**",
        model_info.get(
            "predictive_feature_count",
            "Unknown",
        ),
    )

    st.write(
        "**Target Classes:**",
        model_info.get(
            "target_class_count",
            "Unknown",
        ),
    )

    st.divider()

    st.caption(
        "Educational ML "
        "application. Not a "
        "medical diagnostic tool."
    )


if page == "New Assessment":

    st.info(
        "Enter the requested "
        "information below. The "
        "assessment is processed by "
        "the trained machine "
        "learning pipeline."
    )

    payload = (
        render_assessment_form()
    )

    if payload is not None:

        try:
            with st.spinner(
                "Running obesity risk "
                "assessment..."
            ):
                prediction_result = (
                    api_client.predict(
                        payload
                    )
                )

            st.session_state[
                "prediction_result"
            ] = prediction_result

        except APIClientError as error:
            st.session_state[
                "prediction_result"
            ] = None

            st.error(
                "Prediction request "
                "failed."
            )

            if (
                error.status_code
                is not None
            ):
                st.warning(
                    "Backend response: "
                    f"{str(error)}"
                )

            else:
                st.warning(
                    "The backend API "
                    "could not be reached."
                )

            with st.expander(
                "Technical details"
            ):
                st.code(
                    str(error)
                )

    if (
        st.session_state[
            "prediction_result"
        ]
        is not None
    ):
        current_result = (
            st.session_state[
                "prediction_result"
            ]
        )

        render_prediction_result(
            current_result
        )

        current_prediction_id = (
            current_result.get(
                "prediction_id"
            )
        )

        if (
            current_prediction_id
            is not None
        ):
            st.markdown(
                "### Assessment Report"
            )

            st.write(
                "Download a PDF copy "
                "of this assessment."
            )

            render_pdf_download(
                api_client=api_client,
                prediction_id=(
                    current_prediction_id
                ),
                key_prefix="current",
            )

        else:
            st.warning(
                "No prediction ID was "
                "returned, so a PDF "
                "report cannot be "
                "generated."
            )

        st.button(
            "Start New Assessment",
            on_click=(
                reset_assessment_form
            ),
            type="secondary",
        )


elif page == "Prediction History":

    render_prediction_history(
        api_client
    )


st.divider()

st.caption(
    "The Obesity Risk Intelligence "
    "System is an educational "
    "machine learning application. "
    "Predictions are not medical "
    "diagnoses and should not "
    "replace professional health "
    "assessment."
)