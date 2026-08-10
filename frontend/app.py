import streamlit as st

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


st.title(
    "Obesity Risk "
    "Intelligence System"
)

st.caption(
    "Machine Learning-Based "
    "Obesity Risk Assessment"
)

st.divider()


st.subheader(
    "System Status"
)


try:
    health_data = (
        api_client.get_health()
    )

    model_info = (
        api_client.get_model_info()
    )

    if (
        health_data.get(
            "status"
        )
        == "ok"
    ):
        st.success(
            "Backend API connected"
        )

    else:
        st.warning(
            "Backend API returned "
            "an unexpected status"
        )

    st.subheader(
        "Model Information"
    )

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

    with st.expander(
        "View model details"
    ):
        st.write(
            "Model family:",
            model_info.get(
                "model_family",
                "Unknown",
            ),
        )

        st.write(
            "Configuration:",
            model_info.get(
                "configuration",
                "Unknown",
            ),
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

        st.write(
            "Scikit-learn:",
            model_info.get(
                "scikit_learn_version",
                "Unknown",
            ),
        )

        st.write(
            "Classes:"
        )

        for class_name in (
            model_info.get(
                "target_classes",
                [],
            )
        ):
            st.write(
                f"- {class_name}"
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


st.divider()

st.caption(
    "This application is an "
    "educational machine learning "
    "system and is not a medical "
    "diagnostic tool"
)