from html import escape

import pandas as pd
import streamlit as st

from frontend.category_styles import (
    get_category_style,
)
from frontend.time_utils import (
    format_sri_lanka_datetime,
)


CLASS_LABELS = {
    "Insufficient_Weight":
        "Insufficient Weight",

    "Normal_Weight":
        "Normal Weight",

    "Overweight_Level_I":
        "Overweight Level I",

    "Overweight_Level_II":
        "Overweight Level II",

    "Obesity_Type_I":
        "Obesity Type I",

    "Obesity_Type_II":
        "Obesity Type II",

    "Obesity_Type_III":
        "Obesity Type III",
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


def format_class_name(
    class_name,
):
    return CLASS_LABELS.get(
        class_name,
        str(
            class_name
        ).replace(
            "_",
            " ",
        ),
    )


def build_probability_dataframe(
    probabilities,
):
    rows = []

    for class_name in CLASS_ORDER:
        probability = float(
            probabilities.get(
                class_name,
                0.0,
            )
        )

        rows.append(
            {
                "Category":
                    format_class_name(
                        class_name
                    ),

                "Probability":
                    probability,

                "Probability (%)":
                    probability
                    * 100,
            }
        )

    dataframe = pd.DataFrame(
        rows
    )

    return dataframe.sort_values(
        by="Probability",
        ascending=False,
        ignore_index=True,
    )


def _build_probability_html(
    probabilities,
):
    sorted_classes = sorted(
        CLASS_ORDER,
        key=lambda class_name:
            float(
                probabilities.get(
                    class_name,
                    0.0,
                )
            ),
        reverse=True,
    )

    rows = []

    for class_name in sorted_classes:
        probability = float(
            probabilities.get(
                class_name,
                0.0,
            )
        )

        category = escape(
            format_class_name(
                class_name
            )
        )

        category_style = (
            get_category_style(
                class_name
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

        percentage = (
            probability
            * 100
        )

        bar_width = max(
            0.0,
            min(
                percentage,
                100.0,
            ),
        )

        rows.append(
            f"""
            <div
                class="
                    health-probability-row
                "
                style="
                    border-color:
                    {category_border};

                    background:
                    linear-gradient(
                        90deg,
                        #FFFFFF 0%,
                        #FFFFFF 82%,
                        {category_background} 100%
                    );
                "
            >

                <div
                    class="
                        health-probability-header
                    "
                >

                    <span
                        class="
                            health-probability-name
                        "
                    >
                        {category}
                    </span>

                    <span
                        class="
                            health-probability-value
                        "
                        style="
                            color:
                            {category_color};
                        "
                    >
                        {percentage:.2f}%
                    </span>

                </div>

                <div
                    class="
                        health-probability-track
                    "
                >

                    <div
                        class="
                            health-probability-fill
                        "
                        style="
                            width:
                            {bar_width:.2f}%;

                            background:
                            {category_color};
                        "
                    >
                    </div>

                </div>

            </div>
            """
        )

    return "".join(
        rows
    )


def _get_second_highest_class(
    probabilities,
):
    dataframe = (
        build_probability_dataframe(
            probabilities
        )
    )

    if len(
        dataframe
    ) < 2:
        return None

    return {
        "category":
            dataframe.iloc[
                1
            ][
                "Category"
            ],

        "probability":
            float(
                dataframe.iloc[
                    1
                ][
                    "Probability"
                ]
            ),
    }


def _sanitize_technical_details(
    value,
):
    if isinstance(
        value,
        dict,
    ):
        return {
            key:
                _sanitize_technical_details(
                    item
                )
            for key, item
            in value.items()
            if key not in {
                "id",
                "prediction_id",
            }
        }

    if isinstance(
        value,
        list,
    ):
        return [
            _sanitize_technical_details(
                item
            )
            for item in value
        ]

    return value


def render_prediction_result(
    result,
):
    if not isinstance(
        result,
        dict,
    ):
        st.error(
            "Prediction result "
            "is unavailable."
        )

        return

    required_fields = {
        "predicted_class",
        "confidence",
        "probabilities",
    }

    if not required_fields.issubset(
        result.keys()
    ):
        st.error(
            "Prediction result "
            "is incomplete."
        )

        return

    predicted_class = (
        result[
            "predicted_class"
        ]
    )

    readable_class = (
        format_class_name(
            predicted_class
        )
    )

    risk_info = RISK_LEVEL_MAP.get(
        predicted_class,
        {
            "label": "Unknown",
            "emoji": "⚪",
            "class": "unknown",
        },
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

    confidence = float(
        result[
            "confidence"
        ]
    )

    confidence_percentage = (
        confidence
        * 100
    )

    probabilities = (
        result[
            "probabilities"
        ]
        or {}
    )

    model_name = (
        result.get(
            "model_name"
        )
        or "Unavailable"
    )

    created_at_value = (
        result.get(
            "created_at"
        )
    )

    created_at = (
        format_sri_lanka_datetime(
            created_at_value
        )
        if created_at_value
        else None
    )

    second_highest = (
        _get_second_highest_class(
            probabilities
        )
    )

    if second_highest is None:
        supporting_text = (
            "The model assigned this "
            "category the highest "
            "predicted probability."
        )

    else:
        supporting_text = (
            "The model assigned the "
            "highest probability to "
            f"{readable_class}. The "
            "next most likely category "
            f"was {second_highest['category']} "
            f"at "
            f"{second_highest['probability'] * 100:.2f}%."
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
        (
            "Top Category",
            readable_class,
            "🎯",
            "Highest probability class",
        ),
        (
            "Model",
            str(model_name),
            "🤖",
            "Inference engine",
        ),
        (
            "Classes Evaluated",
            str(len(probabilities)),
            "📊",
            "Multi-class evaluation",
        ),
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
        style="border-color: {category_border};"
    >
        <div class="health-confidence-card-header">
            <span class="health-confidence-kicker">Confidence</span>
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
                        background: {category_color};
                    "
                ></div>
            </div>
            <div class="health-confidence-scale-labels">
                <span>0%</span>
                <span>Model Certainty</span>
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
                background:
                    radial-gradient(circle at 92% 10%, {category_background} 0%, transparent 45%),
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
                                    style="background: {category_color};"
                                ></span>
                                Model-Predicted Category
                            </span>
                            <span class="health-risk-badge {risk_info['class']}">
                                {risk_info["emoji"]} {risk_info["label"]}
                            </span>
                        </div>

                        <div
                            class="health-result-category"
                            style="color: {category_color};"
                        >
                            {escape(readable_class)}
                        </div>
                    </div>

                    <div class="health-result-description-card">
                        <span class="health-result-desc-icon">💡</span>
                        <p class="health-result-desc-text">
                            {escape(supporting_text)}
                        </p>
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
        <section
            class="
                health-probability-section
            "
        >

            <div
                class="
                    health-section-title
                "
            >
                Probability distribution
            </div>

            <div
                class="
                    health-section-description
                "
            >
                The model compares all seven
                obesity-risk categories.
                Longer bars indicate a higher
                predicted probability for the
                submitted assessment.
            </div>

            <div
                class="
                    health-probability-list
                "
            >
                {
                    _build_probability_html(
                        probabilities
                    )
                }
            </div>

        </section>
        """
    )

    probability_sum = sum(
        float(
            value
        )
        for value
        in probabilities.values()
    )

    if abs(
        probability_sum
        - 1.0
    ) > 0.01:
        st.warning(
            "The returned class "
            "probabilities do not sum "
            "to approximately 100%."
        )

    st.html(
        """
        <section class="health-explanation-card">

            <div class="health-section-title">
                Why did the model make this prediction?
            </div>


            <div class="health-section-description">

                The model evaluated 16
                health-related signals from
                your assessment, including
                physical measurements,
                nutrition behaviour, and
                lifestyle patterns.

            </div>


            <div class="health-explanation-grid">


                <div class="health-explanation-item physical">

                    <strong>
                        ⚖ Physical Factors
                    </strong>

                    <br>

                    Age, height, weight,
                    and body measurements.

                </div>


                <div class="health-explanation-item nutrition">

                    <strong>
                        🍎 Nutrition Factors
                    </strong>

                    <br>

                    Eating behaviour,
                    food choices, and
                    hydration patterns.

                </div>


                <div class="health-explanation-item lifestyle">

                    <strong>
                        🏃 Lifestyle Factors
                    </strong>

                    <br>

                    Physical activity,
                    technology use, and
                    daily habits.

                </div>


            </div>


        </section>
        """
    )

    st.html(
        """
        <div class="health-notice">

            <strong>
                How to interpret this result
            </strong>

            <br><br>

            The predicted category is the
            class assigned the highest
            probability by the machine
            learning model.

            Confidence represents model
            certainty for this prediction,
            not medical certainty.

        </div>
        """
    )

    if created_at:
        st.caption(
            f"Assessment recorded: "
            f"{created_at}"
        )

    technical_details = (
        _sanitize_technical_details(
            result
        )
    )

    with st.expander(
        "Technical prediction details"
    ):
        st.json(
            technical_details
        )