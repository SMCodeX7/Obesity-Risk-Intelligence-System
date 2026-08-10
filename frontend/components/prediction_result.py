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
        class_name.replace(
            "_",
            " ",
        ),
    )


def build_probability_dataframe(
    probabilities,
):
    rows = []

    for class_name in CLASS_ORDER:
        probability = (
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
                    float(
                        probability
                    ),

                "Probability (%)":
                    float(
                        probability
                    ) * 100,
            }
        )

    probability_df = (
        pd.DataFrame(
            rows
        )
    )

    probability_df = (
        probability_df
        .sort_values(
            "Probability",
            ascending=False,
        )
        .reset_index(
            drop=True
        )
    )

    return probability_df


def render_prediction_result(
    prediction_result,
):
    if not isinstance(
        prediction_result,
        dict,
    ):
        st.error(
            "The prediction result "
            "has an invalid format"
        )
        return

    predicted_class = (
        prediction_result.get(
            "predicted_class"
        )
    )

    confidence = (
        prediction_result.get(
            "confidence"
        )
    )

    probabilities = (
        prediction_result.get(
            "probabilities",
            {},
        )
    )

    if (
        predicted_class is None
        or confidence is None
        or not isinstance(
            probabilities,
            dict,
        )
    ):
        st.error(
            "The backend returned an "
            "incomplete prediction"
        )
        return

    readable_prediction = (
        format_class_name(
            predicted_class
        )
    )

    probability_df = (
        build_probability_dataframe(
            probabilities
        )
    )

    st.divider()

    st.subheader(
        "Assessment Result"
    )

    col1, col2 = (
        st.columns(2)
    )

    with col1:
        st.metric(
            "Model-Predicted Category",
            readable_prediction,
            border=True,
        )

    with col2:
        st.metric(
            "Prediction Confidence",
            f"{confidence * 100:.2f}%",
            border=True,
        )

    st.progress(
        min(
            max(
                float(confidence),
                0.0,
            ),
            1.0,
        ),
        text=(
            "Model confidence for "
            "the predicted category"
        ),
    )

    st.caption(
        "Confidence represents the "
        "model's predicted probability "
        "for the selected category. "
        "It is not a medical certainty"
    )

    st.markdown(
        "### Class Probability Distribution"
    )

    st.bar_chart(
        probability_df,
        x="Category",
        y="Probability (%)",
        horizontal=True,
        height=420,
    )

    st.markdown(
        "### Probability Ranking"
    )

    display_df = (
        probability_df[
            [
                "Category",
                "Probability (%)",
            ]
        ]
        .copy()
    )

    display_df[
        "Probability (%)"
    ] = (
        display_df[
            "Probability (%)"
        ]
        .map(
            lambda value:
                f"{value:.2f}%"
        )
    )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
    )

    st.markdown(
        "### Result Summary"
    )

    highest_probability = (
        probability_df.iloc[0]
    )

    st.write(
        "The model assigned the "
        "highest probability to "
        f"**{readable_prediction}** "
        "with a confidence of "
        f"**{confidence * 100:.2f}%**."
    )

    if len(
        probability_df
    ) > 1:
        second_result = (
            probability_df.iloc[1]
        )

        st.write(
            "The next highest "
            "predicted category was "
            f"**{second_result['Category']}** "
            "with a probability of "
            f"**{second_result['Probability (%)']:.2f}%**."
        )

    calculated_probability_sum = (
        probability_df[
            "Probability"
        ].sum()
    )

    if abs(
        calculated_probability_sum
        - 1.0
    ) > 0.01:
        st.warning(
            "The returned class "
            "probabilities do not sum "
            "approximately to 100%"
        )

    with st.expander(
        "Technical prediction details"
    ):
        st.write(
            "Raw predicted class:",
            predicted_class,
        )

        st.write(
            "Raw confidence:",
            confidence,
        )

        st.write(
            "Probability sum:",
            calculated_probability_sum,
        )

        st.json(
            prediction_result
        )

    st.info(
        "This result is produced by a "
        "machine learning model for "
        "educational purposes. It is "
        "not a medical diagnosis or "
        "professional health assessment"
    )