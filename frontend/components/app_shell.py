from html import escape

import streamlit as st


def _safe_text(
    value,
    fallback="Unavailable",
):
    if value is None:
        return fallback

    return escape(
        str(value)
    )


def _get_model_metrics(
    model_info,
):
    metrics = (
        model_info.get(
            "final_test_metrics",
            {},
        )
        or {}
    )

    accuracy = metrics.get(
        "accuracy"
    )

    macro_f1 = metrics.get(
        "macro_f1"
    )

    return (
        accuracy,
        macro_f1,
    )


def render_hero(
    model_info,
):
    accuracy, _ = (
        _get_model_metrics(
            model_info
        )
    )

    if accuracy is None:
        accuracy_text = "Available"

    else:
        accuracy_text = (
            f"{accuracy * 100:.2f}%"
        )

    feature_count = (
        model_info.get(
            "predictive_feature_count",
            16,
        )
    )

    target_count = (
        model_info.get(
            "target_class_count",
            7,
        )
    )

    st.html(
        f"""
        <section class="health-hero">

            <div class="health-eyebrow">
                <span class="health-eyebrow-dot"></span>
                <span>AI-Powered · Health Risk Assessment</span>
                <span class="health-eyebrow-badge">Live ML</span>
            </div>

            <h1 class="health-hero-title">
                Understand your
                <span class="health-hero-gradient">
                    health risk profile
                </span>
            </h1>

            <p class="health-hero-description">
                Analyze physical characteristics, nutrition behaviour, and lifestyle
                patterns using an AI-powered obesity-risk classification system.
                Receive prediction confidence, probability insights, assessment
                history, and downloadable reports through an interactive health
                analytics experience.
            </p>

            <div class="health-stats">

                <div class="health-stat">
                    <div class="health-stat-header">
                        <span class="health-stat-tag tag-accent-blue">Calibrated ML</span>
                        <div class="health-stat-icon icon-blue icon-target"></div>
                    </div>
                    <div class="health-stat-body">
                        <span class="health-stat-value">
                            {_safe_text(accuracy_text)}
                        </span>
                        <span class="health-stat-label">
                            Model Accuracy
                        </span>
                    </div>
                    <div class="health-stat-footer">
                        <span class="health-stat-desc">Validated on holdout test set</span>
                    </div>
                </div>

                <div class="health-stat">
                    <div class="health-stat-header">
                        <span class="health-stat-tag tag-accent-teal">Multi-Factor</span>
                        <div class="health-stat-icon icon-teal icon-pulse"></div>
                    </div>
                    <div class="health-stat-body">
                        <span class="health-stat-value">
                            {_safe_text(feature_count)}
                        </span>
                        <span class="health-stat-label">
                            Health Signals
                        </span>
                    </div>
                    <div class="health-stat-footer">
                        <span class="health-stat-desc">Biometric, dietary & lifestyle data</span>
                    </div>
                </div>

                <div class="health-stat">
                    <div class="health-stat-header">
                        <span class="health-stat-tag tag-accent-indigo">Clinical Spectrum</span>
                        <div class="health-stat-icon icon-indigo icon-shield"></div>
                    </div>
                    <div class="health-stat-body">
                        <span class="health-stat-value">
                            {_safe_text(target_count)}
                        </span>
                        <span class="health-stat-label">
                            Risk Categories
                        </span>
                    </div>
                    <div class="health-stat-footer">
                        <span class="health-stat-desc">Stratified WHO classification tiers</span>
                    </div>
                </div>

            </div>

        </section>
        """
    )


def render_navigation(
    show_history=True,
):
    options = [
        "Assessment",
    ]

    if show_history:
        options.append(
            "History"
        )

    selected_page = st.pills(
        "Main navigation",
        options=options,
        default="Assessment",
        selection_mode="single",
        key="main_navigation",
        label_visibility="collapsed",
        width="stretch",
    )

    if selected_page is None:
        return "Assessment"

    return selected_page


def render_page_header(
    kicker,
    title,
    description,
):
    st.html(
        f"""
        <section class="health-page-header">

            <div class="health-page-kicker">
                {_safe_text(kicker)}
            </div>

            <h2 class="health-page-title">
                {_safe_text(title)}
            </h2>

            <p class="health-page-description">
                {_safe_text(description)}
            </p>

        </section>
        """
    )


def render_sidebar(
    health_data,
    model_info,
):
    accuracy, macro_f1 = (
        _get_model_metrics(
            model_info
        )
    )

    model_name = (
        model_info.get(
            "selected_model",
            "Model unavailable",
        )
    )

    feature_count = (
        model_info.get(
            "predictive_feature_count",
            16,
        )
    )

    target_count = (
        model_info.get(
            "target_class_count",
            7,
        )
    )

    api_connected = (
        health_data.get(
            "status"
        )
        == "ok"
    )

    with st.sidebar:

        st.html(
            """
            <div
                class="health-sidebar-brand"
            >

                <div
                    class="health-sidebar-row"
                >

                    <div
                        class="health-sidebar-logo"
                    >
                        ORI
                    </div>

                    <div>

                        <div
                            class="
                                health-sidebar-title
                            "
                        >
                            Obesity Risk
                            Intelligence
                        </div>

                        <div
                            class="
                                health-sidebar-subtitle
                            "
                        >
                            ML Health Assessment
                        </div>

                    </div>

                </div>

            </div>
            """
        )


        st.caption(
            "SYSTEM STATUS"
        )

        if api_connected:

            st.html(
                """
                <div class="health-status">

                    <span
                        class="
                            health-status-dot
                        "
                    >
                    </span>

                    Backend API connected

                </div>
                """
            )

        else:

            st.warning(
                "Backend API unavailable"
            )


        st.divider()


        st.caption(
            "PREDICTION MODEL"
        )

        st.markdown(
            f"**{_safe_text(model_name)}**"
        )

        st.caption(
            "Selected machine learning "
            "classifier"
        )


        st.write("")


        metric_left, metric_right = (
            st.columns(2)
        )


        with metric_left:

            if accuracy is not None:

                st.metric(
                    "Accuracy",
                    (
                        f"{accuracy * 100:.1f}%"
                    ),
                    border=True,
                )

            else:

                st.metric(
                    "Accuracy",
                    "N/A",
                    border=True,
                )


        with metric_right:

            if macro_f1 is not None:

                st.metric(
                    "Macro F1",
                    f"{macro_f1:.3f}",
                    border=True,
                )

            else:

                st.metric(
                    "Macro F1",
                    "N/A",
                    border=True,
                )


        st.divider()


        st.caption(
            "MODEL SCOPE"
        )


        scope_left, scope_right = (
            st.columns(2)
        )


        with scope_left:

            st.metric(
                "Inputs",
                feature_count,
                border=True,
            )


        with scope_right:

            st.metric(
                "Classes",
                target_count,
                border=True,
            )


        st.divider()


        st.html(
            """
            <div class="health-notice">

                <strong>
                    Educational system
                </strong>

                <br><br>

                Predictions describe patterns
                identified by the machine
                learning model and are not
                medical diagnoses.

            </div>
            """
        )


def render_footer():
    st.html(
        """
        <footer class="health-footer">

            <strong>
                Obesity Risk Intelligence
                System
            </strong>

            <br>

            Educational machine learning
            application for obesity-risk
            classification.

            Results should not replace
            professional medical assessment
            or healthcare advice.

        </footer>
        """
    )