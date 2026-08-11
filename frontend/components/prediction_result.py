from html import escape

import pandas as pd
import streamlit as st


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
    dataframe = (
        build_probability_dataframe(
            probabilities
        )
    )

    rows = []

    for _, row in dataframe.iterrows():
        category = escape(
            str(
                row[
                    "Category"
                ]
            )
        )

        probability = float(
            row[
                "Probability"
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

    prediction_id = (
        result.get(
            "prediction_id"
        )
        or result.get(
            "id"
        )
    )

    model_name = (
        result.get(
            "model_name"
        )
    )

    created_at = (
        result.get(
            "created_at"
        )
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

    metadata_items = []

    if prediction_id is not None:
        metadata_items.append(
            (
                "Assessment ID",
                f"#{prediction_id}",
            )
        )

    metadata_items.append(
        (
            "Top Category",
            readable_class,
        )
    )

    if model_name:
        metadata_items.append(
            (
                "Model",
                str(
                    model_name
                ),
            )
        )

    elif len(
        metadata_items
    ) < 3:
        metadata_items.append(
            (
                "Classes Evaluated",
                str(
                    len(
                        probabilities
                    )
                ),
            )
        )

    metadata_html = []

    for (
        label,
        value,
    ) in metadata_items[
        :3
    ]:
        metadata_html.append(
            f"""
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
                    {
                        escape(
                            str(
                                label
                            )
                        )
                    }
                </div>

                <div
                    class="
                        health-result-meta-value
                    "
                >
                    {
                        escape(
                            str(
                                value
                            )
                        )
                    }
                </div>

            </div>
            """
        )

    st.html(
        f"""
        <section
            class="
                health-result-summary
            "
        >

            <div
                class="
                    health-result-top
                "
            >

                <div>

                    <div
                        class="
                            health-result-eyebrow
                        "
                    >
                        Model-Predicted Category
                    </div>

                    <div
                        class="
                            health-result-category
                        "
                    >
                        {
                            escape(
                                readable_class
                            )
                        }
                    </div>

                    <div
                        class="
                            health-result-description
                        "
                    >
                        {
                            escape(
                                supporting_text
                            )
                        }
                    </div>

                </div>


                <div
                    class="
                        health-confidence-box
                    "
                >

                    <div
                        class="
                            health-confidence-label
                        "
                    >
                        Model Confidence
                    </div>

                    <div
                        class="
                            health-confidence-value
                        "
                    >
                        {
                            confidence_percentage
                        :.2f}%
                    </div>

                </div>

            </div>


            <div
                class="
                    health-result-meta
                "
            >
                {
                    "".join(
                        metadata_html
                    )
                }
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

    with st.expander(
        "Technical prediction details"
    ):
        st.json(
            result
        )