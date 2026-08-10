import streamlit as st

from frontend.services.api_client import (
    APIClientError,
)


def render_pdf_download(
    api_client,
    prediction_id,
    key_prefix,
):
    try:
        pdf_bytes = (
            api_client
            .get_prediction_report(
                prediction_id
            )
        )

    except APIClientError as error:
        st.warning(
            "The PDF report could "
            "not be prepared."
        )

        with st.expander(
            "PDF technical details"
        ):
            st.code(
                str(error)
            )

        return

    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name=(
            "obesity-risk-"
            f"assessment-{prediction_id}.pdf"
        ),
        mime="application/pdf",
        key=(
            f"{key_prefix}_"
            f"pdf_{prediction_id}"
        ),
        type="primary",
        width="stretch",
    )