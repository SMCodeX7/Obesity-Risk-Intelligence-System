import streamlit as st

from frontend.components.app_shell import (
    render_footer,
    render_hero,
    render_navigation,
    render_page_header,
    render_sidebar,
)
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
from frontend.config import (
    is_history_ui_enabled,
)
from frontend.services.api_client import (
    APIClient,
    APIClientError,
)
from frontend.styles import (
    load_app_styles,
)


st.set_page_config(
    page_title="Obesity Risk Intelligence",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)


load_app_styles()


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


if (
    "assessment_step"
    not in st.session_state
):
    st.session_state[
        "assessment_step"
    ] = 1


try:
    health_data = (
        api_client.get_health()
    )

    model_info = (
        api_client.get_model_info()
    )

except APIClientError as error:
    st.error(
        "Healthcare assessment service "
        "is currently unavailable."
    )

    st.write(
        "The interface could not "
        "connect to the Flask backend."
    )

    st.info(
        "Start the backend service "
        "and refresh this page."
    )

    with st.expander(
        "Technical details"
    ):
        st.code(
            str(error)
        )

    st.stop()


render_sidebar(
    health_data=health_data,
    model_info=model_info,
)


render_hero(
    model_info=model_info
)


st.write("")


page = render_navigation(
    show_history=(
        is_history_ui_enabled()
    )
)


if page == "Assessment":
    render_page_header(
        kicker="Guided Health Assessment",
        title=(
            "Build your obesity-risk profile"
        ),
        description=(
            "Complete three short sections "
            "covering your physical profile, "
            "nutrition habits, and lifestyle. "
            "Your information is processed by "
            "the trained machine learning "
            "pipeline to estimate an obesity-"
            "risk category."
        ),
    )

    payload = (
        render_assessment_form()
    )

    if payload is not None:
        try:
            with st.spinner(
                "Analyzing your assessment..."
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
                "The assessment could "
                "not be completed."
            )

            if (
                error.status_code
                is not None
            ):
                st.warning(
                    (
                        "Backend response: "
                        f"{str(error)}"
                    )
                )

            else:
                st.warning(
                    "The backend service "
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

        st.write("")

        render_page_header(
            kicker="Assessment Complete",
            title="Your assessment result",
            description=(
                "Review the model's predicted "
                "category, confidence score, "
                "and probability distribution "
                "across all seven obesity-risk "
                "categories."
            ),
        )

        with st.container(
            border=True
        ):
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
                st.divider()

                st.markdown(
                    "#### Assessment report"
                )

                st.caption(
                    "Download a formatted PDF "
                    "copy of this assessment "
                    "for your records."
                )

                render_pdf_download(
                    api_client=api_client,
                    prediction_id=(
                        current_prediction_id
                    ),
                    key_prefix="current",
                )

        st.write("")

        st.html(
            """
            <div class="health-notice">

                <strong>
                    About this result
                </strong>

                <br><br>

                This prediction represents
                patterns learned by a machine
                learning model from its
                training data.

                It is an educational risk
                classification and should
                not be interpreted as a
                medical diagnosis.

            </div>
            """
        )

        st.write("")

        st.button(
            "Start New Assessment",
            on_click=(
                reset_assessment_form
            ),
            type="secondary",
            width="stretch",
        )


elif page == "History":
    render_page_header(
        kicker="Assessment Archive",
        title="Prediction history",
        description=(
            "Review previous assessments, "
            "reopen the information used for "
            "each prediction, examine the "
            "stored result, and download "
            "assessment reports."
        ),
    )

    render_prediction_history(
        api_client
    )


render_footer()