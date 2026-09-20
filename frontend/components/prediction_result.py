from html import escape

import pandas as pd
import streamlit as st

from frontend.category_styles import get_category_style
from frontend.time_utils import format_sri_lanka_datetime


CLASS_LABELS = {
    "Insufficient_Weight": "Insufficient Weight",
    "Normal_Weight": "Normal Weight",
    "Overweight_Level_I": "Overweight Level I",
    "Overweight_Level_II": "Overweight Level II",
    "Obesity_Type_I": "Obesity Type I",
    "Obesity_Type_II": "Obesity Type II",
    "Obesity_Type_III": "Obesity Type III",
}

CLASS_ORDER = [
    "Insufficient_Weight",
    "Normal_Weight",
    "Overweight_Level_I",
    "Overweight_Level_II",
    "Obesity_Type_I",
    "Obesity_Type_II",
    "Obesity_Type_III",
]

RISK_LEVEL_MAP = {
    "Insufficient_Weight": {
        "label": "Low Risk · Underweight",
        "emoji": "🔵",
        "class": "insufficient",
    },
    "Normal_Weight": {
        "label": "Optimal Range · Low Risk",
        "emoji": "🟢",
        "class": "low",
    },
    "Overweight_Level_I": {
        "label": "Moderate Risk · Grade I",
        "emoji": "🟡",
        "class": "moderate",
    },
    "Overweight_Level_II": {
        "label": "Elevated Risk · Grade II",
        "emoji": "🟠",
        "class": "moderate-high",
    },
    "Obesity_Type_I": {
        "label": "High Risk · Class I",
        "emoji": "🔴",
        "class": "high",
    },
    "Obesity_Type_II": {
        "label": "Very High Risk · Class II",
        "emoji": "🔴",
        "class": "very-high",
    },
    "Obesity_Type_III": {
        "label": "Severe Clinical Risk · Class III",
        "emoji": "🚨",
        "class": "severe",
    },
}


def format_class_name(class_name):
    return CLASS_LABELS.get(class_name, str(class_name).replace("_", " "))


def build_probability_dataframe(probabilities):
    rows = []
    for class_name in CLASS_ORDER:
        probability = float(probabilities.get(class_name, 0.0))
        rows.append(
            {
                "Category": format_class_name(class_name),
                "Probability": probability,
                "Probability (%)": probability * 100,
            }
        )

    dataframe = pd.DataFrame(rows)
    return dataframe.sort_values(by="Probability", ascending=False, ignore_index=True)


def _build_probability_html(probabilities, predicted_class=None):
    sorted_classes = sorted(
        CLASS_ORDER,
        key=lambda class_name: float(probabilities.get(class_name, 0.0)),
        reverse=True,
    )

    rows = []
    for rank, class_name in enumerate(sorted_classes, start=1):
        probability = float(probabilities.get(class_name, 0.0))
        category = escape(format_class_name(class_name))
        category_style = get_category_style(class_name)
        category_color = category_style["color"]
        category_background = category_style["background"]
        category_border = category_style["border"]

        percentage = probability * 100
        min_visual_pct = 1.0 if probability > 0 else 0.0
        bar_width = max(min_visual_pct, min(percentage, 100.0))

        is_top = (rank == 1)
        is_predicted = (class_name == predicted_class)
        row_class = "health-probability-row"

        if is_top:
            row_class += " health-prob-row--top"
        if is_predicted:
            row_class += " health-prob-row--predicted"

        if rank == 1:
            rank_badge = '<span class="health-prob-rank health-prob-rank--gold">#1</span>'
        elif rank == 2:
            rank_badge = '<span class="health-prob-rank health-prob-rank--silver">#2</span>'
        elif rank == 3:
            rank_badge = '<span class="health-prob-rank health-prob-rank--bronze">#3</span>'
        else:
            rank_badge = f'<span class="health-prob-rank">#{rank}</span>'

        risk_info = RISK_LEVEL_MAP.get(class_name, {})
        raw_risk_label = risk_info.get("label", "")
        risk_tag = raw_risk_label.split("·")[0].strip() if "·" in raw_risk_label else raw_risk_label

        if is_predicted and is_top:
            selected_indicator = (
                f'<span class="health-prob-selected-badge" style="background: {category_background}; '
                f'color: {category_color}; border: 1px solid {category_border};">★ Highest Probability · Primary Prediction</span>'
            )
        elif is_predicted:
            selected_indicator = (
                f'<span class="health-prob-selected-badge" style="background: {category_background}; '
                f'color: {category_color}; border: 1px solid {category_border};">✓ Selected Prediction</span>'
            )
        elif is_top:
            selected_indicator = (
                f'<span class="health-prob-crown" style="background: {category_background}; '
                f'color: {category_color}; border: 1px solid {category_border};" title="Highest Probability">★ Highest Probability</span>'
            )
        else:
            selected_indicator = ""

        if is_predicted:
            row_inline_style = (
                f"border-color: {category_color}; "
                f"border-left: 4px solid {category_color}; "
                f"background: linear-gradient(90deg, {category_background} 0%, rgba(255, 255, 255, 0.96) 24%, #FFFFFF 100%); "
                f"box-shadow: 0 6px 20px -3px rgba(15, 23, 42, 0.08), 0 0 0 1px {category_border};"
            )
        elif is_top:
            row_inline_style = (
                f"border-color: {category_border}; "
                f"border-left: 4px solid {category_color}; "
                f"background: linear-gradient(90deg, {category_background} 0%, rgba(255, 255, 255, 0.98) 20%, #FFFFFF 100%); "
                f"box-shadow: 0 4px 16px -4px rgba(15, 23, 42, 0.06), 0 0 0 1px {category_border};"
            )
        else:
            row_inline_style = (
                "border-color: rgba(226, 232, 240, 0.85); "
                "background: #FFFFFF;"
            )

        val_extra_class = " health-prob-val--top" if is_top else ""
        fill_extra_style = (
            f"box-shadow: 0 0 8px {category_color}55; "
            if (is_top or is_predicted)
            else ""
        )

        rows.append(
            f"""
            <div
                class="{row_class}"
                style="{row_inline_style}"
            >
                <div class="health-probability-header">
                    <div class="health-prob-name-group">
                        {rank_badge}
                        <span
                            class="health-prob-dot"
                            style="
                                background: {category_color};
                                box-shadow: 0 0 0 3px {category_background};
                            "
                        ></span>
                        <span
                            class="health-probability-name{' health-prob-name--top' if is_top else ''}{' health-prob-name--predicted' if is_predicted else ''}"
                            style="{'color: ' + category_color + ';' if (is_top or is_predicted) else ''}"
                        >
                            {category}
                        </span>
                        <span
                            class="health-prob-risk-tag"
                            style="
                                background: {category_background};
                                color: {category_color};
                                border: 1px solid {category_border};
                            "
                        >
                            {escape(risk_tag)}
                        </span>
                        {selected_indicator}
                    </div>

                    <div class="health-prob-val-group">
                        <span
                            class="health-probability-value{val_extra_class}"
                            style="color: {category_color};"
                        >
                            {percentage:.2f}%
                        </span>
                    </div>
                </div>

                <div class="health-probability-track">
                    <div
                        class="health-probability-fill{' health-prob-fill--top' if is_top else ''}{' health-prob-fill--predicted' if is_predicted else ''}"
                        style="
                            width: {bar_width:.2f}%;
                            background: {category_color};
                            {fill_extra_style}
                        "
                    ></div>
                </div>
            </div>
            """
        )

    return "".join(rows)


def _get_second_highest_class(probabilities):
    dataframe = build_probability_dataframe(probabilities)
    if len(dataframe) < 2:
        return None

    return {
        "category": dataframe.iloc[1]["Category"],
        "probability": float(dataframe.iloc[1]["Probability"]),
    }


def _sanitize_technical_details(value):
    if isinstance(value, dict):
        return {
            key: _sanitize_technical_details(item)
            for key, item in value.items()
            if key not in {"id", "prediction_id"}
        }

    if isinstance(value, list):
        return [_sanitize_technical_details(item) for item in value]

    return value


def render_prediction_result(result):
    if not isinstance(result, dict):
        st.error("Prediction result is unavailable.")
        return

    required_fields = {
        "predicted_class",
        "confidence",
        "probabilities",
    }

    if not required_fields.issubset(result.keys()):
        st.error("Prediction result is incomplete.")
        return

    predicted_class = result["predicted_class"]
    readable_class = format_class_name(predicted_class)

    risk_info = RISK_LEVEL_MAP.get(
        predicted_class,
        {
            "label": "Unknown",
            "emoji": "⚪",
            "class": "unknown",
        },
    )

    category_style = get_category_style(predicted_class)
    category_color = category_style["color"]
    category_background = category_style["background"]
    category_border = category_style["border"]

    confidence = float(result["confidence"])
    confidence_percentage = confidence * 100
    probabilities = result.get("probabilities") or {}
    model_name = result.get("model_name") or "Unavailable"

    created_at_value = result.get("created_at")
    created_at = format_sri_lanka_datetime(created_at_value) if created_at_value else None

    second_highest = _get_second_highest_class(probabilities)

    if second_highest is None:
        supporting_text = (
            "The model assigned this category the highest predicted probability."
        )
    else:
        supporting_text = (
            f"The model assigned the highest probability to {readable_class}. "
            f"The next most likely category was {second_highest['category']} "
            f"at {second_highest['probability'] * 100:.2f}%."
        )

    if confidence_percentage >= 90:
        certainty_level = "Very High"
    elif confidence_percentage >= 75:
        certainty_level = "High"
    elif confidence_percentage >= 50:
        certainty_level = "Moderate"
    else:
        certainty_level = "Low"

    metadata_items = [
        ("Top Category", readable_class, "🎯", "Highest probability class"),
        ("Model", str(model_name), "🤖", "Inference engine"),
        ("Classes Evaluated", str(len(probabilities)), "📊", "Multi-class evaluation"),
    ]

    metadata_html = []
    for label, value, icon, subtext in metadata_items:
        metadata_html.append(
            f"""
            <div class="health-result-meta-item">
                <div class="health-meta-icon-box">{icon}</div>
                <div class="health-meta-content">
                    <div class="health-result-meta-label">{escape(str(label))}</div>
                    <div class="health-result-meta-value" title="{escape(str(value))}">{escape(str(value))}</div>
                    <div class="health-meta-sub">{escape(str(subtext))}</div>
                </div>
            </div>
            """
        )

    confidence_card_html = f"""
    <div
        class="health-confidence-card"
        style="
            border-color: {category_border};
            border-top: 3.5px solid {category_color};
            box-shadow: 0 8px 24px -4px rgba(15, 23, 42, 0.07), 0 0 0 1px {category_border};
        "
    >
        <div class="health-confidence-card-header">
            <span class="health-confidence-kicker">Model Certainty</span>
            <span
                class="health-confidence-badge"
                style="
                    background: {category_background};
                    color: {category_color};
                    border: 1px solid {category_border};
                "
            >
                {certainty_level}
            </span>
        </div>

        <div class="health-confidence-dial-wrap">
            <div
                class="health-confidence-dial"
                style="
                    background: conic-gradient(
                        {category_color} 0% {confidence_percentage:.1f}%,
                        #E2E8F0 {confidence_percentage:.1f}% 100%
                    );
                "
            >
                <div class="health-confidence-dial-inner">
                    <div
                        class="health-confidence-number"
                        style="color: {category_color};"
                    >
                        {confidence_percentage:.1f}<span class="health-confidence-pct-sign">%</span>
                    </div>
                    <div class="health-confidence-caption">Certainty</div>
                </div>
            </div>
        </div>

        <div class="health-confidence-meter-container">
            <div class="health-confidence-bar-track">
                <div
                    class="health-confidence-bar-fill"
                    style="
                        width: {max(0.0, min(confidence_percentage, 100.0)):.1f}%;
                        background: linear-gradient(90deg, {category_color}cc, {category_color});
                        box-shadow: 0 0 8px {category_color}45;
                    "
                ></div>
            </div>
            <div class="health-confidence-scale-labels">
                <span>0%</span>
                <span class="health-confidence-scale-title">Calibrated Confidence</span>
                <span>100%</span>
            </div>
        </div>
    </div>
    """

    st.html(
        f"""
        <section
            class="health-result-summary"
            style="
                border-color: {category_border};
                border-top: 4px solid {category_color};
                background:
                    radial-gradient(circle at 92% 10%, {category_background} 0%, transparent 48%),
                    linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 55%, {category_background} 100%);
            "
        >
            <div class="health-result-top">
                <div class="health-result-main-col">
                    <div>
                        <div class="health-result-eyebrow-row">
                            <span class="health-result-eyebrow">
                                <span
                                    class="health-result-live-dot"
                                    style="
                                        background: {category_color};
                                        box-shadow: 0 0 0 3px {category_background};
                                    "
                                ></span>
                                AI Diagnostic Assessment
                            </span>
                            <span
                                class="health-risk-badge {risk_info['class']}"
                                style="
                                    background: {category_background};
                                    color: {category_color};
                                    border: 1px solid {category_border};
                                "
                            >
                                {risk_info["emoji"]} {risk_info["label"]}
                            </span>
                        </div>

                        <div class="health-result-category-container">
                            <div class="health-result-category-kicker">Predicted Classification</div>
                            <div
                                class="health-result-category"
                                style="color: {category_color};"
                            >
                                {escape(readable_class)}
                            </div>
                        </div>
                    </div>

                    <div
                        class="health-result-description-card"
                        style="border-left: 3px solid {category_color};"
                    >
                        <span class="health-result-desc-icon" style="color: {category_color};">💡</span>
                        <div class="health-result-desc-body">
                            <div class="health-result-desc-label">Assessment Rationale</div>
                            <p class="health-result-desc-text">
                                {escape(supporting_text)}
                            </p>
                        </div>
                    </div>
                </div>

                {confidence_card_html}
            </div>

            <div class="health-result-meta">
                {"".join(metadata_html)}
            </div>
        </section>
        """
    )

    st.html(
        f"""
        <section class="health-probability-section">
            <div class="health-prob-section-header">
                <div class="health-prob-header-left">
                    <span class="health-prob-kicker">Multi-Class Spectrum</span>
                    <div class="health-section-title">
                        Probability Distribution
                    </div>
                    <div class="health-section-description">
                        Comparative probability evaluated across all seven obesity-risk categories.
                        Ranked in descending order of model confidence.
                    </div>
                </div>
                <div class="health-prob-header-badge">
                    <span class="health-prob-count-pill">7 Classes Evaluated</span>
                </div>
            </div>

            <div class="health-probability-list">
                {_build_probability_html(probabilities, predicted_class=predicted_class)}
            </div>
        </section>
        """
    )

    probability_sum = sum(float(value) for value in probabilities.values())

    if abs(probability_sum - 1.0) > 0.01:
        st.warning("The returned class probabilities do not sum to approximately 100%.")

    st.html(
        """
        <section class="health-explanation-card">
            <div class="health-explanation-header">
                <span class="health-explanation-kicker">Clinical Signal Attribution</span>
                <div class="health-section-title">
                    Why did the model make this prediction?
                </div>
                <div class="health-section-description">
                    The AI system evaluated 16 multidimensional health signals from
                    your assessment, spanning physical measurements, nutritional patterns,
                    and lifestyle behaviours.
                </div>
            </div>

            <div class="health-explanation-grid">
                <div class="health-explanation-item physical">
                    <div>
                        <div class="health-module-code">Module 01 · Anthropometric</div>
                        <div class="health-explanation-item-header">
                            <div class="health-explanation-item-icon">⚖️</div>
                            <span class="health-factor-badge physical">5 Signals</span>
                        </div>
                        <div class="health-explanation-item-body">
                            <div class="health-explanation-item-title">
                                Physical Measurements
                            </div>
                            <div class="health-explanation-item-desc">
                                Age, height, weight, BMI metrics, and family history indicators.
                            </div>
                            <div class="health-signal-chips">
                                <span class="health-signal-chip">Age & Gender</span>
                                <span class="health-signal-chip">Height & Weight</span>
                                <span class="health-signal-chip">BMI Metric</span>
                                <span class="health-signal-chip">Family History</span>
                            </div>
                        </div>
                    </div>
                    <div class="health-module-impact">
                        <span class="health-impact-label">Clinical Impact</span>
                        <span class="health-impact-pill physical">Primary Determinant</span>
                    </div>
                </div>

                <div class="health-explanation-item nutrition">
                    <div>
                        <div class="health-module-code">Module 02 · Dietary Patterns</div>
                        <div class="health-explanation-item-header">
                            <div class="health-explanation-item-icon">🍎</div>
                            <span class="health-factor-badge nutrition">6 Signals</span>
                        </div>
                        <div class="health-explanation-item-body">
                            <div class="health-explanation-item-title">
                                Nutrition & Hydration
                            </div>
                            <div class="health-explanation-item-desc">
                                Meal frequency, vegetable consumption, calorie-dense foods, and fluid intake.
                            </div>
                            <div class="health-signal-chips">
                                <span class="health-signal-chip">Caloric Food (FAVC)</span>
                                <span class="health-signal-chip">Vegetable Intake (FCVC)</span>
                                <span class="health-signal-chip">Meal Count (NCP)</span>
                                <span class="health-signal-chip">Hydration (CH2O)</span>
                                <span class="health-signal-chip">Snacking (CAEC)</span>
                            </div>
                        </div>
                    </div>
                    <div class="health-module-impact">
                        <span class="health-impact-label">Clinical Impact</span>
                        <span class="health-impact-pill nutrition">High Contribution</span>
                    </div>
                </div>

                <div class="health-explanation-item lifestyle">
                    <div>
                        <div class="health-module-code">Module 03 · Behavioural Dynamics</div>
                        <div class="health-explanation-item-header">
                            <div class="health-explanation-item-icon">🏃</div>
                            <span class="health-factor-badge lifestyle">5 Signals</span>
                        </div>
                        <div class="health-explanation-item-body">
                            <div class="health-explanation-item-title">
                                Lifestyle & Activity
                            </div>
                            <div class="health-explanation-item-desc">
                                Physical exercise frequency, screen time duration, and daily mobility habits.
                            </div>
                            <div class="health-signal-chips">
                                <span class="health-signal-chip">Exercise Freq (FAF)</span>
                                <span class="health-signal-chip">Screen Time (TUE)</span>
                                <span class="health-signal-chip">Commute (MTRANS)</span>
                                <span class="health-signal-chip">Smoking Status</span>
                                <span class="health-signal-chip">Alcohol (CALC)</span>
                            </div>
                        </div>
                    </div>
                    <div class="health-module-impact">
                        <span class="health-impact-label">Clinical Impact</span>
                        <span class="health-impact-pill lifestyle">Behavioural Factor</span>
                    </div>
                </div>
            </div>
        </section>
        """
    )

    st.html(
        """
        <div class="health-result-notice">
            <div class="health-result-notice-icon">🔬</div>
            <div class="health-result-notice-body">
                <div class="health-result-notice-title">
                    Clinical Result Interpretation Guide
                </div>
                <div class="health-result-notice-text">
                    The predicted category represents the highest probability class
                    assigned by the machine learning classification model. Confidence
                    reflects statistical algorithm certainty for this specific feature profile,
                    intended for clinical decision support and health risk stratification.
                </div>
            </div>
        </div>
        """
    )

    if created_at:
        st.caption(f"Assessment recorded: {created_at}")

    technical_details = _sanitize_technical_details(result)

    with st.expander("Technical Prediction Details"):
        st.json(technical_details)