import streamlit as st

from frontend.components.assessment_form import (
    render_assessment_form,
)
from frontend.components.prediction_result import (
    render_prediction_result,
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


st.title(
    "Obesity Risk "
    "Intelligence System"
)

st.caption(
    "Machine Learning-Based "
    "Obesity Risk Assessment"
)

st.divider()


try:
    health_data = (
        api_client.get_health()
    )

    model_info = (
        api_client.get_model_info()
    )

except APIClientError as error:
    st.error(
        "Backend API is unavailable"
    )

    st.info(
        "Start the Flask backend "
        "and refresh this page"
    )

    with st.expander(
        "Technical details"
    ):
        st.code(
            str(error)
        )

    st.stop()


if (
    health_data.get(
        "status"
    )
    == "ok"
):
    st.success(
        "Backend API connected"
    )


with st.expander(
    "Model Information"
):
    col1, col2, col3 = (
        st.columns(3)
    )

    with col1:
        st.metric(
            "Model",
            model_info.get(
                "selected_model",
                "Unknown",
            ),
        )

    with col2:
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

        if accuracy is not None:
            st.metric(
                "Test Accuracy",
                f"{accuracy * 100:.2f}%",
            )

        else:
            st.metric(
                "Test Accuracy",
                "Unavailable",
            )

    with col3:
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

        if macro_f1 is not None:
            st.metric(
                "Macro F1",
                f"{macro_f1:.4f}",
            )

        else:
            st.metric(
                "Macro F1",
                "Unavailable",
            )

    st.write(
        "Input features:",
        model_info.get(
            "predictive_feature_count",
            "Unknown",
        ),
    )

    st.write(
        "Target classes:",
        model_info.get(
            "target_class_count",
            "Unknown",
        ),
    )


st.divider()


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
        st.error(
            "Prediction request failed"
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
    render_prediction_result(
        st.session_state[
            "prediction_result"
        ]
    )


st.divider()

st.caption(
    "This application is an "
    "educational machine learning "
    "system and is not a medical "
    "diagnostic tool"
)