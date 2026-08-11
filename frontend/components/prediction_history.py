import json
from html import escape

import pandas as pd
import streamlit as st

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

    latest_category = (
        format_class_name(
            latest.get(
                "predicted_class",
                "Unavailable",
            )
        )
        if latest
        else "Unavailable"
    )

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
        <section
            class="health-history-summary"
        >

            <div
                class="health-history-stat"
            >

                <div
                    class="
                        health-history-stat-value
                    "
                >
                    {count}
                </div>

                <div
                    class="
                        health-history-stat-label
                    "
                >
                    Saved Assessments
                </div>

            </div>


            <div
                class="health-history-stat"
            >

                <div
                    class="
                        health-history-stat-value
                    "
                >
                    {
                        _safe_text(
                            latest_category
                        )
                    }
                </div>

                <div
                    class="
                        health-history-stat-label
                    "
                >
                    Latest Category
                </div>

            </div>


            <div
                class="health-history-stat"
            >

                <div
                    class="
                        health-history-stat-value
                    "
                >
                    {
                        _safe_text(
                            highest_confidence
                        )
                    }
                </div>

                <div
                    class="
                        health-history-stat-label
                    "
                >
                    Highest Confidence
                </div>

            </div>

        </section>
        """
    )


def _render_history_cards(
    predictions,
):
    cards = []

    for prediction in predictions:
        prediction_id = (
            prediction.get(
                "id",
                "Unavailable",
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

        confidence = (
            _format_percentage(
                prediction.get(
                    "confidence"
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

        model_name = (
            prediction.get(
                "model_name",
                "Unavailable",
            )
        )

        cards.append(
            f"""
            <article
                class="health-history-card"
            >

                <div
                    class="
                        health-history-header
                    "
                >

                    <div
                        class="
                            health-history-id
                        "
                    >
                        Assessment
                        #{_safe_text(prediction_id)}
                    </div>

                    <div
                        class="
                            health-history-date
                        "
                    >
                        {_safe_text(created_at)}
                    </div>

                </div>


                <div
                    class="
                        health-history-category
                    "
                >
                    {_safe_text(category)}
                </div>


                <div
                    class="
                        health-history-details
                    "
                >

                    <span>
                        Confidence
                        <strong>
                            {_safe_text(confidence)}
                        </strong>
                    </span>

                    <span>
                        Model
                        <strong>
                            {_safe_text(model_name)}
                        </strong>
                    </span>

                </div>

            </article>
            """
        )

    st.html(
        f"""
        <section
            class="health-history-list"
        >
            {"".join(cards)}
        </section>
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
        f"Assessment #{prediction_id} "
        f"— {category} "
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
                Assessment
                #{_safe_text(selected_id)}
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