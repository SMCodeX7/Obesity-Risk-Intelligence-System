import streamlit as st

from frontend.services.api_client import APIClientError


def render_pdf_download(api_client, prediction_id, key_prefix):
    if prediction_id is None:
        st.warning(
            "A PDF report is not available because the assessment ID could not be found."
        )
        return

    try:
        pdf_bytes = api_client.get_prediction_report(prediction_id)
    except APIClientError as error:
        st.warning("The PDF report could not be prepared.")
        with st.expander("Technical Details"):
            st.code(str(error))
        return

    st.html(
        f"""
        <section class="health-report-card">
            <div class="health-report-header">
                <div class="health-report-icon" aria-label="PDF Document">
                    <div class="health-report-doc-badge">
                        <span class="health-report-doc-symbol">📄</span>
                        <span class="health-report-pdf-pill">PDF</span>
                    </div>
                </div>
                <div class="health-report-header-text">
                    <div class="health-report-title-row">
                        <div class="health-report-title">
                            Assessment Report
                        </div>
                        <span class="health-report-ready-badge">Ready</span>
                    </div>
                    <div class="health-report-subtitle">
                        Comprehensive clinical summary including AI risk classification, probability distribution, anthropometric baseline, and lifestyle guidance.
                    </div>
                </div>
            </div>

            <div class="health-report-features">
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-blue"></span>
                    <span class="health-report-feature-name">AI prediction result</span>
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-teal"></span>
                    <span class="health-report-feature-name">Confidence score</span>
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-indigo"></span>
                    <span class="health-report-feature-name">Probability distribution</span>
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-cyan"></span>
                    <span class="health-report-feature-name">Assessment inputs</span>
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-amber"></span>
                    <span class="health-report-feature-name">Model analysis details</span>
                </div>
                <div class="health-report-feature">
                    <span class="health-report-feature-dot dot-green"></span>
                    <span class="health-report-feature-name">Educational context</span>
                </div>
            </div>
        </section>
        """
    )

    st.download_button(
        label="Download PDF Report",
        data=pdf_bytes,
        file_name=f"obesity-risk-assessment-{prediction_id}.pdf",
        mime="application/pdf",
        key=f"{key_prefix}_pdf_{prediction_id}",
        type="primary",
        width="stretch",
    )

