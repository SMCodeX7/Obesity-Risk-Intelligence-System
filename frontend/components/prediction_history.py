import json
from html import escape

import altair as alt
import pandas as pd
import streamlit as st

from frontend.category_styles import (
    get_category_style,
)
from frontend.components.prediction_result import (
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

    for index, prediction in enumerate(predictions):
        is_latest = (index == 0)

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
            '<span class="health-vtl-latest-badge">Latest</span>'
            if is_latest
            else ""
        )

        is_last = (index == len(predictions) - 1)
        connector = (
            ""
            if is_last
            else '<div class="health-vtl-connector"></div>'
        )

        items.append(
            f"""
            <div class="health-vtl-item">
                <div class="health-vtl-rail">
                    <div
                        class="health-vtl-dot{'  health-vtl-dot--latest' if is_latest else ''}"
                        style="
                            background: {category_color};
                            box-shadow: 0 0 0 4px {category_background},
                                        0 0 0 6px {category_border};
                        "
                    ></div>
                    {connector}
                </div>

                <div
                    class="health-vtl-card{'  health-vtl-card--latest' if is_latest else ''}"
                    style="border-color: {category_border};"
                >
                    <div class="health-vtl-card-top">
                        <div class="health-vtl-date-row">
                            <span class="health-vtl-date">
                                🕐 {_safe_text(created_at)}
                            </span>
                            {latest_badge}
                        </div>

                        <div
                            class="health-vtl-category"
                            style="color: {category_color};"
                        >
                            {_safe_text(category)}
                        </div>
                    </div>

                    <div class="health-vtl-meta-row">
                        <div class="health-vtl-confidence-block">
                            <div class="health-vtl-meta-label">Confidence</div>
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

    return (
        f"{category} "
        f"— {created_at}"
    )


def _render_detail_group(
    title,
    feature_names,
    inputs,
):
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

        cards.append(
            f"""
            <div
                class="health-detail-card"
            >

                <div
                    class="
                        health-detail-title
                    "
                >
                    {_safe_text(label)}
                </div>

                <div
                    class="
                        health-detail-value
                    "
                >
                    {_safe_text(value)}
                </div>

            </div>
            """
        )

    st.markdown(
        f"#### {title}"
    )

    st.html(
        f"""
        <section
            class="health-detail-grid"
        >
            {"".join(cards)}
        </section>
        """
    )


def _render_assessment_inputs(
    inputs,
):
    st.html(
        """
        <div
            class="health-section-title"
        >
            Submitted assessment
        </div>

        <div
            class="
                health-section-description
            "
        >
            These are the 16 input values
            stored with this prediction.
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
    )

    st.write("")

    _render_detail_group(
        title="Nutrition",
        feature_names=(
            NUTRITION_FEATURES
        ),
        inputs=inputs,
    )

    st.write("")

    _render_detail_group(
        title="Lifestyle",
        feature_names=(
            LIFESTYLE_FEATURES
        ),
        inputs=inputs,
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

    st.html(
        f"""
        <section
            class="health-result-summary"
        >

            <div
                class="
                    health-result-eyebrow
                "
            >
                Saved Assessment
            </div>

            <div
                class="
                    health-result-category
                "
            >
                Assessment Details
            </div>

            <div
                class="
                    health-result-description
                "
            >
                Review the information used
                for this saved prediction,
                inspect the model output,
                and access the stored report.
            </div>


            <div
                class="health-result-meta"
            >

                <div
                    class="
                        health-result-meta-item
                    "
                >

                    <div
                        class="
                            health-result-meta-label
                        "
                    >
                        Recorded
                    </div>

                    <div
                        class="
                            health-result-meta-value
                        "
                    >
                        {_safe_text(created_at)}
                    </div>

                </div>


                <div
                    class="
                        health-result-meta-item
                    "
                >

                    <div
                        class="
                            health-result-meta-label
                        "
                    >
                        Model
                    </div>

                    <div
                        class="
                            health-result-meta-value
                        "
                    >
                        {_safe_text(model_name)}
                    </div>

                </div>


                <div
                    class="
                        health-result-meta-item
                    "
                >

                    <div
                        class="
                            health-result-meta-label
                        "
                    >
                        Scikit-learn
                    </div>

                    <div
                        class="
                            health-result-meta-value
                        "
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
        <div
            class="health-section-title"
        >
            Recent assessments
        </div>

        <div
            class="
                health-section-description
            "
        >
            Saved predictions are displayed
            with the newest assessment first.
            Select one below to inspect its
            complete details.
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

    st.markdown(
        "### Open an assessment"
    )

    st.caption(
        "Select a saved assessment "
        "to review its complete input "
        "profile and model result."
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