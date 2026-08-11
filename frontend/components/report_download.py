from html import escape

import streamlit as st

from frontend.services.api_client import (
    APIClientError,
)


def render_pdf_download(
    api_client,
    prediction_id,
    key_prefix,
):
    if prediction_id is None:
        st.warning(
            "A PDF report is not available "
            "because the assessment ID "
            "could not be found."
        )

        return

    try:
        pdf_bytes = (
            api_client.get_prediction_report(
                prediction_id
            )
        )

    except APIClientError as error:
        st.warning(
            "The PDF report could "
            "not be prepared."
        )

        with st.expander(
            "Technical details"
        ):
            st.code(
                str(
                    error
                )
            )

        return

    safe_prediction_id = escape(
        str(
            prediction_id
        )
    )

    st.html(
        f"""
        <div
            class="health-info-card"
        >

            <div
                class="health-info-icon"
            >
                PDF
            </div>

            <div
                class="health-info-title"
            >
                Assessment report ready
            </div>

            <div
                class="health-info-text"
            >
                A formatted PDF report has
                been prepared for assessment
                #{safe_prediction_id}.

                It includes the submitted
                assessment information,
                predicted category,
                confidence score, and model
                probability information.
            </div>

        </div>
        """
    )

    st.download_button(
        label="Download Assessment Report",
        data=pdf_bytes,
        file_name=(
            "obesity-risk-assessment-"
            f"{prediction_id}.pdf"
        ),
        mime="application/pdf",
        key=(
            f"{key_prefix}_pdf_"
            f"{prediction_id}"
        ),
        type="primary",
        width="stretch",
    )