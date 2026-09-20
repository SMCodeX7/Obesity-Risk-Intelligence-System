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


    st.html(
        f"""
        <section class="health-report-card">

            <!-- ── Card header ── -->
            <div class="health-report-header">

                <div class="health-report-icon">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="1.8"
                         stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12
                                 a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                        <line x1="16" y1="13" x2="8" y2="13"/>
                        <line x1="16" y1="17" x2="8" y2="17"/>
                        <polyline points="10 9 9 9 8 9"/>
                    </svg>
                </div>

                <div class="health-report-header-text">
                    <div class="health-report-title">
                        Assessment Report
                        <span class="health-report-ready-badge">Ready</span>
                    </div>
                    <div class="health-report-subtitle">
                        Complete AI obesity-risk summary · PDF format
                    </div>
                </div>

            </div>

            <!-- ── Feature grid ── -->
            <div class="health-report-features">

                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-blue"></span>
                    AI prediction result
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-teal"></span>
                    Confidence score
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-blue"></span>
                    Probability distribution
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-teal"></span>
                    Assessment inputs
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-blue"></span>
                    Model analysis details
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-teal"></span>
                    Educational context
                </div>

            </div>

        </section>
        """
    )

    st.download_button(
        label="⬇  Download PDF Report",
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
