import json
from html import escape

import altair as alt
import pandas as pd
import streamlit as st

from frontend.category_styles import (
    get_category_style,
)
from frontend.components.prediction_result import (
    RISK_LEVEL_MAP,
    format_class_name,
    render_prediction_result,
)
from frontend.components.report_download import (
    render_pdf_download,
)
from frontend.services.api_client import (
    APIClientError,
)
from frontend.time_utils import (
    format_sri_lanka_datetime,
    format_sri_lanka_datetime_compact,
)

CATEGORY_COLOR_SCALE = alt.Scale(
    domain=[
        "Normal Weight",
        "Insufficient Weight",
        "Overweight Level I",
        "Overweight Level II",
        "Obesity Type I",
        "Obesity Type II",
        "Obesity Type III",
        "Unavailable",
    ],
    range=[
        "#16A34A",  # Normal Weight = green
        "#0284C7",  # Insufficient Weight = blue
        "#D97706",  # Overweight Level I = amber
        "#EA580C",  # Overweight Level II = orange
        "#E11D48",  # Obesity Type I = red
        "#DC2626",  # Obesity Type II = red
        "#991B1B",  # Obesity Type III = dark red
        "#64748B",  # Unavailable = gray
    ],
)


FEATURE_LABELS = {
    "Age": "Age",
    "Height": "Height",
    "Weight": "Weight",
    "Gender": "Gender",
    "family_history_with_overweight":
        "Family History of Overweight",
    "FCVC": "Vegetable Consumption Score",
    "NCP": "Main Meal Score",
    "CAEC": "Food Between Meals",
    "FAVC":
        "Frequent High-Calorie Food",
    "CH2O": "Water Consumption Score",
    "CALC": "Alcohol Consumption",
    "FAF": "Physical Activity Score",
    "TUE": "Technology Use Score",
    "SMOKE": "Smoking",
    "SCC": "Calorie Monitoring",
    "MTRANS":
        "Primary Transportation",
}


PROFILE_FEATURES = [
    "Age",
    "Height",
    "Weight",
    "Gender",
    "family_history_with_overweight",
]


NUTRITION_FEATURES = [
    "FCVC",
    "NCP",
    "CAEC",
    "FAVC",
    "CH2O",
    "CALC",
]


LIFESTYLE_FEATURES = [
    "FAF",
    "TUE",
    "SMOKE",
    "SCC",
    "MTRANS",
]


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
                            "Unavailable",
                        )
                    ),

                "Confidence":
                    f"{confidence * 100:.2f}%",

                "Model":
                    prediction.get(
                        "model_name",
                        "Unavailable",
                    ),

                "Created At":
                    prediction.get(
                        "created_at",
                        "Unavailable",
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

    for (
        feature,
        label,
    ) in FEATURE_LABELS.items():
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


def _safe_text(
    value,
    fallback="Unavailable",
):
    if (
        value is None
        or value == ""
    ):
        value = fallback

    return escape(
        str(
            value
        )
    )


def _format_percentage(
    value,
):
    try:
        return (
            f"{float(value) * 100:.2f}%"
        )

    except (
        TypeError,
        ValueError,
    ):
        return "Unavailable"


def _render_empty_state():
    st.html(
        """
        <section
            class="health-empty-state"
        >

            <div
                class="health-empty-icon"
            >
                00
            </div>

            <div
                class="health-empty-title"
            >
                No saved assessments yet
            </div>

            <div
                class="health-empty-text"
            >
                Complete your first obesity-risk
                assessment and the prediction
                will automatically appear here
                for future review.
            </div>

        </section>
        """
    )


def _reset_history_ui_state():
    keys = [
        "selected_history_prediction_id",
        "history_prediction_selector",
        "show_history_clear_confirmation",
        "confirm_history_clear",
    ]

    for key in keys:
        st.session_state.pop(
            key,
            None,
        )


def _render_clear_history_controls(
    api_client,
    prediction_count,
):
    st.write("")

    with st.expander(
        "History management"
    ):
        st.markdown(
            "#### Clear prediction history"
        )

        st.caption(
            "Remove all saved prediction "
            "records from the history. "
            "This action cannot be undone."
        )

        confirmation_open = (
            st.session_state.get(
                "show_history_clear_confirmation",
                False,
            )
        )

        if not confirmation_open:
            if st.button(
                "Clear prediction history",
                key="open_history_clear_confirmation",
                width="stretch",
            ):
                st.session_state[
                    "show_history_clear_confirmation"
                ] = True

                st.rerun()

            return

        st.warning(
            f"This will permanently delete "
            f"all {prediction_count} saved "
            f"assessment records."
        )

        confirmed = st.checkbox(
            (
                "I understand that all saved "
                "prediction history will be "
                "permanently deleted."
            ),
            key="confirm_history_clear",
        )

        cancel_column, clear_column = (
            st.columns(
                2
            )
        )

        with cancel_column:
            if st.button(
                "Cancel",
                key="cancel_history_clear",
                width="stretch",
            ):
                st.session_state.pop(
                    "show_history_clear_confirmation",
                    None,
                )

                st.session_state.pop(
                    "confirm_history_clear",
                    None,
                )

                st.rerun()

        with clear_column:
            if st.button(
                "Permanently clear history",
                key="confirm_history_clear_button",
                disabled=not confirmed,
                type="primary",
                width="stretch",
            ):
                try:
                    response = (
                        api_client.clear_predictions()
                    )

                except APIClientError as error:
                    if (
                        error.status_code
                        == 403
                    ):
                        st.error(
                            "Prediction history "
                            "clearing is disabled "
                            "on this backend."
                        )

                    else:
                        st.error(
                            "Prediction history "
                            "could not be cleared."
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

                deleted_count = (
                    response.get(
                        "deleted_count",
                        prediction_count,
                    )
                    if isinstance(
                        response,
                        dict,
                    )
                    else prediction_count
                )

                _reset_history_ui_state()

                st.session_state[
                    "history_clear_success"
                ] = (
                    f"{deleted_count} saved "
                    f"assessment record"
                    f"{'' if deleted_count == 1 else 's'} "
                    f"cleared."
                )

                st.rerun()


def _render_history_analytics(
    predictions,
):
    if not predictions:
        return

    dataframe = pd.DataFrame(
        [
            {
                "Date":
                    format_sri_lanka_datetime_compact(
                        prediction.get(
                            "created_at"
                        )
                    ),

                "Confidence":
                    float(
                        prediction.get(
                            "confidence",
                            0.0,
                        )
                    )
                    * 100,

                "Category":
                    format_class_name(
                        prediction.get(
                            "predicted_class",
                            "Unavailable",
                        )
                    ),
            }

            for prediction in reversed(
                predictions
            )
        ]
    )

    st.html(
        f"""
        <div class="health-analytics-header">
            <div class="health-analytics-header-left">
                <span class="health-analytics-kicker">Clinical Pattern Intelligence</span>
                <div class="health-section-title">
                    Assessment Analytics
                </div>
                <div class="health-section-description">
                    Longitudinal confidence trend tracking and risk category frequency analysis across historical evaluations.
                </div>
            </div>
            <div class="health-analytics-header-right">
                <span class="health-analytics-count-pill">{len(predictions)} Assessments Evaluated</span>
            </div>
        </div>
        """
    )

    column1, column2 = st.columns(
        2,
        gap="large",
    )

    with column1:

        st.html(
            """
            <div class="health-chart-card-header">
                <div class="health-chart-header-left">
                    <span class="health-chart-kicker">Longitudinal Trajectory</span>
                    <div class="health-chart-title">Confidence Trend</div>
                    <div class="health-chart-subtitle">Chronological progression of model certainty per assessment</div>
                </div>
                <span class="health-chart-badge">0% – 100% Scale</span>
            </div>
            """
        )

        confidence_data = (
            dataframe.copy()
        )

        confidence_data[
            "Assessment"
        ] = range(
            1,
            len(confidence_data) + 1,
        )

        base = alt.Chart(
            confidence_data
        )

        confidence_line = (
            base.mark_line(
                strokeWidth=3,
                color="#2563EB",
                interpolate="monotone",
            )
            .encode(
                x=alt.X(
                    "Assessment:O",
                    title="Assessment Sequence",
                    axis=alt.Axis(
                        labelAngle=0,
                        labelFont="Plus Jakarta Sans, sans-serif",
                        titleFont="Plus Jakarta Sans, sans-serif",
                        titleFontSize=11,
                        grid=False,
                    ),
                ),
                y=alt.Y(
                    "Confidence:Q",
                    title="Model Confidence (%)",
                    scale=alt.Scale(
                        domain=[
                            0,
                            100,
                        ]
                    ),
                    axis=alt.Axis(
                        labelFont="Plus Jakarta Sans, sans-serif",
                        titleFont="Plus Jakarta Sans, sans-serif",
                        titleFontSize=11,
                        gridColor="#F1F5F9",
                    ),
                ),
            )
        )

        confidence_points = (
            base.mark_circle(
                size=80,
                opacity=1,
                stroke="#FFFFFF",
                strokeWidth=2,
            )
            .encode(
                x=alt.X("Assessment:O"),
                y=alt.Y("Confidence:Q"),
                color=alt.Color(
                    "Category:N",
                    scale=CATEGORY_COLOR_SCALE,
                    title="Risk Category",
                ),
                tooltip=[
                    alt.Tooltip(
                        "Assessment:O",
                        title="Assessment #",
                    ),
                    alt.Tooltip(
                        "Date:N",
                        title="Recorded",
                    ),
                    alt.Tooltip(
                        "Category:N",
                        title="Predicted Class",
                    ),
                    alt.Tooltip(
                        "Confidence:Q",
                        title="Confidence (%)",
                        format=".2f",
                    ),
                ],
            )
        )

        confidence_chart = (
            (confidence_line + confidence_points)
            .properties(
                height=300,
            )
            .configure_view(
                strokeWidth=0,
            )
            .configure_legend(
                orient="bottom",
                labelFont="Plus Jakarta Sans, sans-serif",
                titleFont="Plus Jakarta Sans, sans-serif",
                columns=2,
            )
        )

        st.altair_chart(
            confidence_chart,
            use_container_width=True,
        )


    with column2:

        st.html(
            """
            <div class="health-chart-card-header">
                <div class="health-chart-header-left">
                    <span class="health-chart-kicker">Frequency Spectrum</span>
                    <div class="health-chart-title">Risk Category Distribution</div>
                    <div class="health-chart-subtitle">Stratified assessment count across obesity classifications</div>
                </div>
                <span class="health-chart-badge">Categorical Total</span>
            </div>
            """
        )

        category_counts = (
            dataframe[
                "Category"
            ]
            .value_counts()
            .rename_axis(
                "Category"
            )
            .reset_index(
                name="Assessments"
            )
        )

        category_chart = (
            alt.Chart(
                category_counts
            )
            .mark_bar(
                cornerRadiusEnd=6,
                height=22,
            )
            .encode(
                x=alt.X(
                    "Assessments:Q",
                    title="Number of Assessments",
                    axis=alt.Axis(
                        tickMinStep=1,
                        format="d",
                        labelFont="Plus Jakarta Sans, sans-serif",
                        titleFont="Plus Jakarta Sans, sans-serif",
                        titleFontSize=11,
                        gridColor="#F1F5F9",
                    ),
                ),
                y=alt.Y(
                    "Category:N",
                    title=None,
                    sort="-x",
                    axis=alt.Axis(
                        labelLimit=200,
                        labelFont="Plus Jakarta Sans, sans-serif",
                    ),
                ),
                color=alt.Color(
                    "Category:N",
                    scale=CATEGORY_COLOR_SCALE,
                    legend=None,
                ),
                tooltip=[
                    alt.Tooltip(
                        "Category:N",
                        title="Category",
                    ),
                    alt.Tooltip(
                        "Assessments:Q",
                        title="Assessments",
                        format="d",
                    ),
                ],
            )
            .properties(
                height=300,
            )
            .configure_view(
                strokeWidth=0,
            )
        )

        st.altair_chart(
            category_chart,
            use_container_width=True,
        )

    st.html(
        """
        <div class="health-timeline-section-header">
            <div class="health-timeline-header-left">
                <span class="health-timeline-kicker">Chronological Archive</span>
                <div class="health-section-title">
                    Assessment Timeline
                </div>
                <div class="health-section-description">
                    Sequential log of individual clinical assessments ordered from newest to oldest.
                </div>
            </div>
        </div>
        """
    )

    timeline_cards = []

    for prediction in predictions:
        predicted_class = (
            prediction.get(
                "predicted_class",
                "Unavailable",
            )
        )

        category = (
            format_class_name(
                predicted_class
            )
        )

        category_style = (
            get_category_style(
                predicted_class
            )
        )

        category_color = (
            category_style[
                "color"
            ]
        )

        category_background = (
            category_style[
                "background"
            ]
        )

        category_border = (
            category_style[
                "border"
            ]
        )

        confidence = (
            _format_percentage(
                prediction.get(
                    "confidence"
                )
            )
        )

        date = (
            format_sri_lanka_datetime(
                prediction.get(
                    "created_at"
                )
            )
        )

        model_name = (
            prediction.get(
                "model_name",
                "Unavailable",
            )
        )

        timeline_cards.append(
            f"""
            <article
                class="health-timeline-card"
                style="
                    border-color:
                    {category_border};

                    border-left:
                    5px solid
                    {category_color};

                    background:
                    linear-gradient(
                        90deg,
                        {category_background} 0%,
                        #FFFFFF 18%,
                        #FFFFFF 100%
                    );
                "
            >

                <div
                    class="health-timeline-header"
                >

                    <div
                        class="health-timeline-date"
                    >
                        {_safe_text(date)}
                    </div>

                    <div
                        class="health-timeline-badge"
                        style="
                            background:
                            {category_background};

                            color:
                            {category_color};

                            border:
                            1px solid
                            {category_border};
                        "
                    >
                        {_safe_text(category)}
                    </div>

                </div>

                <div
                    class="health-timeline-footer"
                >

                    <div
                        class="health-timeline-chip"
                    >
                        Confidence
                        <strong>
                            {_safe_text(confidence)}
                        </strong>
                    </div>

                    <div
                        class="health-timeline-chip"
                    >
                        Model
                        <strong>
                            {_safe_text(model_name)}
                        </strong>
                    </div>

                </div>

            </article>
            """
        )

    st.html(
        f"""
        <section
            class="health-timeline-list"
        >
            {"".join(timeline_cards)}
        </section>
        """
    )


def _render_history_summary(
    predictions,
):
    count = len(
        predictions
    )

    latest = (
        predictions[0]
        if predictions
        else {}
    )

    latest_predicted_class = (
        latest.get(
            "predicted_class",
            "Unavailable",
        )
        if latest
        else "Unavailable"
    )

    latest_category = (
        format_class_name(
            latest_predicted_class
        )
        if latest
        else "Unavailable"
    )

    latest_style = (
        get_category_style(
            latest_predicted_class
        )
        if latest_predicted_class != "Unavailable"
        else {
            "color": "#2563EB",
            "background": "#EFF6FF",
            "border": "#BFDBFE",
        }
    )
    latest_cat_color = latest_style["color"]
    latest_cat_bg = latest_style["background"]
    latest_cat_border = latest_style["border"]

    confidence_values = []

    for prediction in predictions:
        try:
            confidence_values.append(
                float(
                    prediction.get(
                        "confidence",
                        0.0,
                    )
                )
            )

        except (
            TypeError,
            ValueError,
        ):
            continue

    if confidence_values:
        highest_confidence = (
            f"{max(confidence_values) * 100:.2f}%"
        )

    else:
        highest_confidence = (
            "Unavailable"
        )

    st.html(
        f"""
        <section class="health-history-summary">

            <div class="health-history-stat health-history-stat--count">
                <div class="health-history-stat-top">
                    <span class="health-history-stat-kicker">Archive Volume</span>
                    <div class="health-history-stat-icon health-stat-icon--blue">📊</div>
                </div>
                <div class="health-history-stat-value">
                    {count}
                </div>
                <div class="health-history-stat-label">
                    Saved Assessments
                </div>
                <div class="health-history-stat-sub">
                    Historical patient profiles
                </div>
            </div>

            <div
                class="health-history-stat health-history-stat--category"
                style="
                    border-top: 3.5px solid {latest_cat_color};
                "
            >
                <div class="health-history-stat-top">
                    <span class="health-history-stat-kicker">Most Recent Result</span>
                    <div
                        class="health-history-stat-icon"
                        style="
                            background: {latest_cat_bg};
                            color: {latest_cat_color};
                            border: 1px solid {latest_cat_border};
                        "
                    >
                        🎯
                    </div>
                </div>
                <div
                    class="health-history-stat-value health-history-stat-val--cat"
                    style="color: {latest_cat_color};"
                    title="{escape(str(latest_category))}"
                >
                    {_safe_text(latest_category)}
                </div>
                <div class="health-history-stat-label">
                    Latest Category
                </div>
                <div class="health-history-stat-sub">
                    Last evaluated classification
                </div>
            </div>

            <div class="health-history-stat health-history-stat--confidence">
                <div class="health-history-stat-top">
                    <span class="health-history-stat-kicker">Peak Certainty</span>
                    <div class="health-history-stat-icon health-stat-icon--teal">⚡</div>
                </div>
                <div class="health-history-stat-value health-history-stat-val--conf">
                    {_safe_text(highest_confidence)}
                </div>
                <div class="health-history-stat-label">
                    Highest Confidence
                </div>
                <div class="health-history-stat-sub">
                    Maximum recorded model score
                </div>
            </div>

        </section>
        """
    )


def _render_history_cards(
    predictions,
):
    items = []
    total_count = len(predictions)

    for index, prediction in enumerate(predictions):
        is_latest = (index == 0)
        seq_num = total_count - index

        predicted_class = (
            prediction.get(
                "predicted_class",
                "Unavailable",
            )
        )

        category = (
            format_class_name(
                predicted_class
            )
        )

        category_style = (
            get_category_style(
                predicted_class
            )
        )

        category_color = category_style["color"]
        category_background = category_style["background"]
        category_border = category_style["border"]

        risk_info = RISK_LEVEL_MAP.get(
            predicted_class,
            {
                "label": "Health Assessment",
                "emoji": "🩺",
                "class": "low",
            },
        )
        risk_label = risk_info.get("label", "Assessment")
        risk_class = risk_info.get("class", "low")

        raw_confidence = prediction.get("confidence", 0.0)
        try:
            confidence_pct = float(raw_confidence) * 100
        except (TypeError, ValueError):
            confidence_pct = 0.0

        confidence_text = _format_percentage(raw_confidence)

        created_at = (
            format_sri_lanka_datetime_compact(
                prediction.get("created_at")
            )
        )

        model_name = prediction.get("model_name", "Unavailable")
        bar_width = max(0.0, min(confidence_pct, 100.0))

        latest_badge = (
            f"""
            <span
                class="health-vtl-latest-badge"
                style="background: linear-gradient(135deg, {category_color} 0%, #0F172A 140%);"
            >
                <span class="health-vtl-pulse-dot"></span>
                Latest Record
            </span>
            """
            if is_latest
            else ""
        )

        is_last = (index == total_count - 1)
        connector = (
            ""
            if is_last
            else '<div class="health-vtl-connector"></div>'
        )

        card_border_left = "5.5px" if is_latest else "4px"
        card_class = (
            f"health-vtl-card{'  health-vtl-card--latest' if is_latest else ''}"
        )
        card_style = (
            f"border-color: {category_border}; "
            f"border-left: {card_border_left} solid {category_color}; "
            f"background: linear-gradient(135deg, {category_background} 0%, rgba(255, 255, 255, 0.98) 28%, #FFFFFF 100%);"
        )

        dot_shadow = (
            f"0 0 0 4px {category_background}, 0 0 0 7px {category_border}, 0 4px 12px rgba(0, 0, 0, 0.08)"
            if is_latest
            else f"0 0 0 3px {category_background}, 0 0 0 5px {category_border}"
        )

        items.append(
            f"""
            <div class="health-vtl-item">
                <div class="health-vtl-rail">
                    <div
                        class="health-vtl-dot{'  health-vtl-dot--latest' if is_latest else ''}"
                        style="
                            background: {category_color};
                            box-shadow: {dot_shadow};
                        "
                    ></div>
                    {connector}
                </div>

                <div
                    class="{card_class}"
                    style="{card_style}"
                >
                    <div class="health-vtl-card-top">
                        <div class="health-vtl-date-row">
                            <span class="health-vtl-seq-badge">#{seq_num}</span>
                            <span class="health-vtl-date">
                                📅 {_safe_text(created_at)}
                            </span>
                            {latest_badge}
                        </div>

                        <div class="health-vtl-category-wrap">
                            <div
                                class="health-vtl-category"
                                style="color: {category_color};"
                            >
                                {_safe_text(category)}
                            </div>
                            <span
                                class="health-vtl-risk-tag health-risk-badge {risk_class}"
                            >
                                {_safe_text(risk_label)}
                            </span>
                        </div>
                    </div>

                    <div class="health-vtl-meta-row">
                        <div class="health-vtl-confidence-block">
                            <div class="health-vtl-meta-label">AI Confidence Score</div>
                            <div class="health-vtl-confidence-bar-wrap">
                                <div class="health-vtl-bar-track">
                                    <div
                                        class="health-vtl-bar-fill"
                                        style="
                                            width: {bar_width:.1f}%;
                                            background: {category_color};
                                        "
                                    ></div>
                                </div>
                                <span
                                    class="health-vtl-confidence-value"
                                    style="color: {category_color};"
                                >
                                    {_safe_text(confidence_text)}
                                </span>
                            </div>
                        </div>

                        <div class="health-vtl-chip">
                            <span class="health-vtl-chip-icon">⚙️</span>
                            <span class="health-vtl-chip-label">Model</span>
                            <span class="health-vtl-chip-value">
                                {_safe_text(model_name)}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            """
        )

    st.html(
        f"""
        <div class="health-vtl-container">
            {"".join(items)}
        </div>
        """
    )


def _format_selector_option(
    prediction_id,
    predictions_by_id,
):
    prediction = (
        predictions_by_id.get(
            prediction_id,
            {},
        )
    )

    category = (
        format_class_name(
            prediction.get(
                "predicted_class",
                "Unavailable",
            )
        )
    )

    created_at = (
        format_sri_lanka_datetime_compact(
            prediction.get(
                "created_at"
            )
        )
    )

    raw_conf = prediction.get("confidence")
    conf_str = (
        f" · {_format_percentage(raw_conf)}"
        if raw_conf is not None
        else ""
    )

    return (
        f"Record #{prediction_id} — "
        f"{category}{conf_str} "
        f"({created_at})"
    )


DETAIL_GROUP_CONFIG = {
    "profile": {
        "theme": "profile",
        "icon": "👤",
        "kicker": "Personal Profile",
        "title": "Demographic & Anthropometric Attributes",
        "description": "Biological characteristics, body measurements, and family history.",
        "badge": "5 Parameters",
        "card_class": "health-detail-card--profile",
    },
    "nutrition": {
        "theme": "nutrition",
        "icon": "🥗",
        "kicker": "Nutrition Habits",
        "title": "Dietary Patterns & Consumption",
        "description": "Food consumption frequency, caloric density, meal pacing, and hydration.",
        "badge": "6 Parameters",
        "card_class": "health-detail-card--nutrition",
    },
    "lifestyle": {
        "theme": "lifestyle",
        "icon": "⚡",
        "kicker": "Lifestyle Factors",
        "title": "Physical Activity & Behaviors",
        "description": "Daily movement, sedentary screen duration, smoking habits, and commute mode.",
        "badge": "5 Parameters",
        "card_class": "health-detail-card--lifestyle",
    },
}


def _render_detail_group(
    title,
    feature_names,
    inputs,
    group_key=None,
):
    if group_key is None:
        group_key = title.lower()

    config = DETAIL_GROUP_CONFIG.get(
        group_key,
        {
            "theme": "profile",
            "icon": "📋",
            "kicker": title,
            "title": title,
            "description": "Recorded clinical input parameters.",
            "badge": f"{len(feature_names)} Parameters",
            "card_class": "health-detail-card--profile",
        },
    )

    theme = config["theme"]
    icon = config["icon"]
    kicker = config["kicker"]
    group_title = config["title"]
    description = config["description"]
    badge = config["badge"]
    card_class = config["card_class"]

    cards = []

    for feature in feature_names:
        label = (
            FEATURE_LABELS.get(
                feature,
                feature,
            )
        )

        value = (
            inputs.get(
                feature,
                "Unavailable",
            )
        )

        if feature == "MTRANS":
            value = str(
                value
            ).replace(
                "_",
                " ",
            )

        if value == "yes":
            value = "Yes"
        elif value == "no":
            value = "No"

        # Format numeric floats with standard units
        if isinstance(value, float):
            if feature == "Height":
                value_display = f"{value:.2f} m"
            elif feature == "Weight":
                value_display = f"{value:.1f} kg"
            elif feature == "Age":
                value_display = (
                    f"{int(value)} yrs"
                    if value.is_integer()
                    else f"{value:.1f} yrs"
                )
            else:
                value_display = f"{value:.2f}".rstrip("0").rstrip(".")
        else:
            value_display = str(value)

        cards.append(
            f"""
            <div class="health-detail-card {card_class}">
                <div class="health-detail-title">
                    {_safe_text(label)}
                </div>
                <div class="health-detail-value">
                    {_safe_text(value_display)}
                </div>
            </div>
            """
        )

    st.html(
        f"""
        <div class="health-detail-group-header health-detail-group-header--{theme}">
            <div class="health-detail-group-icon">{icon}</div>
            <div class="health-detail-group-info">
                <span class="health-detail-group-kicker">{kicker}</span>
                <div class="health-detail-group-title">{group_title}</div>
                <div class="health-detail-group-desc">{description}</div>
            </div>
            <span class="health-detail-group-badge {theme}">{badge}</span>
        </div>

        <section class="health-detail-grid">
            {"".join(cards)}
        </section>
        """
    )


def _render_assessment_inputs(
    inputs,
):
    st.html(
        """
        <div class="health-inputs-section-header">
            <div class="health-inputs-header-left">
                <span class="health-inputs-kicker">Clinical Input Profile</span>
                <div class="health-page-title" style="font-size: 1.35rem; margin-top: 0.15rem;">
                    Submitted Assessment Parameters
                </div>
                <div class="health-page-description" style="font-size: 0.84rem; margin-top: 0.25rem;">
                    All 16 clinical parameters stored for this assessment, grouped into biological profile, nutritional habits, and behavioral lifestyle factors.
                </div>
            </div>
            <span class="health-inputs-count-pill">16 Parameters Recorded</span>
        </div>
        """
    )

    st.write("")

    _render_detail_group(
        title="Profile",
        feature_names=(
            PROFILE_FEATURES
        ),
        inputs=inputs,
        group_key="profile",
    )

    st.write("")

    _render_detail_group(
        title="Nutrition",
        feature_names=(
            NUTRITION_FEATURES
        ),
        inputs=inputs,
        group_key="nutrition",
    )

    st.write("")

    _render_detail_group(
        title="Lifestyle",
        feature_names=(
            LIFESTYLE_FEATURES
        ),
        inputs=inputs,
        group_key="lifestyle",
    )


def _extract_probabilities(
    sources,
):
    for source in sources:
        if not isinstance(
            source,
            dict,
        ):
            continue

        probabilities = (
            source.get(
                "probabilities"
            )
        )

        if isinstance(
            probabilities,
            dict,
        ):
            return probabilities

        if isinstance(
            probabilities,
            str,
        ):
            try:
                parsed = json.loads(
                    probabilities
                )

                if isinstance(
                    parsed,
                    dict,
                ):
                    return parsed

            except json.JSONDecodeError:
                pass

    for source in sources:
        if not isinstance(
            source,
            dict,
        ):
            continue

        probabilities_json = (
            source.get(
                "probabilities_json"
            )
        )

        if isinstance(
            probabilities_json,
            dict,
        ):
            return probabilities_json

        if isinstance(
            probabilities_json,
            str,
        ):
            try:
                parsed = json.loads(
                    probabilities_json
                )

                if isinstance(
                    parsed,
                    dict,
                ):
                    return parsed

            except json.JSONDecodeError:
                pass

    for source in sources:
        if not isinstance(
            source,
            dict,
        ):
            continue

        probability_distribution = (
            source.get(
                "probability_distribution"
            )
        )

        if isinstance(
            probability_distribution,
            dict,
        ):
            return (
                probability_distribution
            )

        if isinstance(
            probability_distribution,
            str,
        ):
            try:
                parsed = json.loads(
                    probability_distribution
                )

                if isinstance(
                    parsed,
                    dict,
                ):
                    return parsed

            except json.JSONDecodeError:
                pass

    return {}


def _prepare_result(
    detail,
    selected_id,
):
    result = {}

    nested_result = (
        detail.get(
            "result"
        )
        if isinstance(
            detail,
            dict,
        )
        else None
    )

    nested_prediction = (
        detail.get(
            "prediction"
        )
        if isinstance(
            detail,
            dict,
        )
        else None
    )

    sources = [
        nested_result,
        nested_prediction,
        detail,
    ]

    for source in sources:
        if not isinstance(
            source,
            dict,
        ):
            continue

        for key in [
            "predicted_class",
            "confidence",
            "model_name",
            "scikit_learn_version",
            "created_at",
        ]:
            if (
                result.get(
                    key
                )
                is None
                and source.get(
                    key
                )
                is not None
            ):
                result[
                    key
                ] = source[
                    key
                ]

    result[
        "probabilities"
    ] = (
        _extract_probabilities(
            sources
        )
    )

    result[
        "prediction_id"
    ] = (
        result.get(
            "prediction_id"
        )
        or (
            detail.get(
                "prediction_id"
            )
            if isinstance(
                detail,
                dict,
            )
            else None
        )
        or (
            detail.get(
                "id"
            )
            if isinstance(
                detail,
                dict,
            )
            else None
        )
        or selected_id
    )

    return result


def _render_detail_header(
    detail,
    selected_id,
):
    result = (
        detail.get(
            "result",
            {}
        )
        or {}
    )

    predicted_class = (
        detail.get("predicted_class")
        or result.get("predicted_class")
    )

    created_at = (
        format_sri_lanka_datetime(
            detail.get(
                "created_at"
            )
            or result.get(
                "created_at"
            )
        )
    )

    model_name = (
        detail.get(
            "model_name"
        )
        or result.get(
            "model_name"
        )
        or "Unavailable"
    )

    version = (
        detail.get(
            "scikit_learn_version"
        )
        or result.get(
            "scikit_learn_version"
        )
        or "Unavailable"
    )

    category_title = "Assessment Details"
    header_style = ""
    eyebrow_text = f"Saved Assessment · Record #{selected_id}"

    if predicted_class:
        category_name = format_class_name(predicted_class)
        category_title = f"Assessment Details: {category_name}"
        cat_style = get_category_style(predicted_class)
        header_style = (
            f"border-top: 4px solid {cat_style['color']}; "
            f"border-color: {cat_style['border']}; "
            f"background: radial-gradient(circle at 95% 8%, {cat_style['background']} 0%, #FFFFFF 65%);"
        )

    st.html(
        f"""
        <section
            class="health-result-summary"
            style="{header_style}"
        >

            <div
                class="health-result-eyebrow"
            >
                {_safe_text(eyebrow_text)}
            </div>

            <div
                class="health-result-category"
            >
                {_safe_text(category_title)}
            </div>

            <div
                class="health-result-description"
            >
                Review the clinical parameters captured for this saved prediction,
                inspect the model output, and access the stored clinical report.
            </div>

            <div
                class="health-result-meta"
            >

                <div
                    class="health-result-meta-item"
                >
                    <div
                        class="health-result-meta-label"
                    >
                        Recorded
                    </div>
                    <div
                        class="health-result-meta-value"
                    >
                        {_safe_text(created_at)}
                    </div>
                </div>

                <div
                    class="health-result-meta-item"
                >
                    <div
                        class="health-result-meta-label"
                    >
                        Model
                    </div>
                    <div
                        class="health-result-meta-value"
                    >
                        {_safe_text(model_name)}
                    </div>
                </div>

                <div
                    class="health-result-meta-item"
                >
                    <div
                        class="health-result-meta-label"
                    >
                        Scikit-learn
                    </div>
                    <div
                        class="health-result-meta-value"
                    >
                        {_safe_text(version)}
                    </div>
                </div>

            </div>

        </section>
        """
    )


def render_prediction_history(
    api_client,
):
    try:
        history_response = (
            api_client.get_predictions()
        )

    except APIClientError as error:
        st.error(
            "Prediction history could "
            "not be loaded."
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

    success_message = (
        st.session_state.pop(
            "history_clear_success",
            None,
        )
    )

    if success_message:
        st.success(
            success_message
        )

    predictions = (
        history_response.get(
            "predictions",
            []
        )
        or []
    )

    if not predictions:
        _render_empty_state()

        return

    _render_history_summary(
        predictions
    )

    st.write("")

    _render_history_analytics(
        predictions
    )

    st.write("")

    _render_clear_history_controls(
        api_client=api_client,
        prediction_count=len(
            predictions
        ),
    )

    st.html(
        """
        <div class="health-timeline-section-header">
            <div class="health-timeline-header-left">
                <span class="health-timeline-kicker">Chronological Archive</span>
                <div class="health-page-title" style="font-size: 1.35rem; margin-top: 0.15rem;">
                    Recent Assessments Timeline
                </div>
                <div class="health-page-description" style="font-size: 0.84rem; margin-top: 0.25rem;">
                    Saved predictions are displayed in chronological order with the latest evaluation highlighted.
                    Browse below or select any assessment to view complete clinical parameters.
                </div>
            </div>
        </div>
        """
    )

    _render_history_cards(
        predictions
    )

    st.write("")

    prediction_ids = [
        prediction.get(
            "id"
        )
        for prediction
        in predictions
        if prediction.get(
            "id"
        )
        is not None
    ]

    if not prediction_ids:
        return

    predictions_by_id = {
        prediction[
            "id"
        ]:
            prediction

        for prediction
        in predictions

        if prediction.get(
            "id"
        )
        is not None
    }

    default_id = (
        st.session_state.get(
            "selected_history_prediction_id"
        )
    )

    if (
        default_id
        not in prediction_ids
    ):
        default_id = (
            prediction_ids[0]
        )

    default_index = (
        prediction_ids.index(
            default_id
        )
    )

    st.divider()

    st.html(
        f"""
        <div class="health-browser-card">
            <div class="health-browser-header">
                <div class="health-browser-icon-box">📁</div>
                <div class="health-browser-content">
                    <span class="health-browser-kicker">Saved Health Record Browser</span>
                    <div class="health-browser-title">Assessment Record Inspector</div>
                    <div class="health-browser-desc">
                        Select a past assessment from your history archive to inspect all 16 clinical risk parameters, review the machine learning model classification, and download clinical PDF reports.
                    </div>
                </div>
                <div class="health-browser-count-badge">
                    {len(prediction_ids)} Record{'s' if len(prediction_ids) != 1 else ''} Available
                </div>
            </div>
        </div>
        """
    )

    selected_id = (
        st.selectbox(
            "Saved assessment",
            options=prediction_ids,
            index=default_index,
            format_func=lambda value:
                _format_selector_option(
                    value,
                    predictions_by_id,
                ),
            key=(
                "history_prediction_selector"
            ),
        )
    )

    st.session_state[
        "selected_history_prediction_id"
    ] = selected_id

    try:
        detail = (
            api_client.get_prediction(
                selected_id
            )
        )

    except APIClientError as error:
        st.error(
            "The selected assessment "
            "could not be loaded."
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

    inputs = (
        detail.get(
            "inputs",
            {}
        )
        or {}
    )

    result = (
        _prepare_result(
            detail,
            selected_id,
        )
    )

    st.write("")

    _render_detail_header(
        detail=detail,
        selected_id=selected_id,
    )

    st.write("")

    _render_assessment_inputs(
        inputs
    )

    with st.expander(
        "View inputs as table"
    ):
        st.dataframe(
            build_input_dataframe(
                inputs
            ),
            width="stretch",
            hide_index=True,
        )

    st.write("")

    st.divider()

    st.markdown(
        "### Model result"
    )

    render_prediction_result(
        result
    )

    st.write("")

    st.divider()

    st.markdown(
        "### Assessment report"
    )

    st.caption(
        "Download the saved PDF report "
        "for this assessment."
    )

    render_pdf_download(
        api_client=api_client,
        prediction_id=selected_id,
        key_prefix="history",
    )