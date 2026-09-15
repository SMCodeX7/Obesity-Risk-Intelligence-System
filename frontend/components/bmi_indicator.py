import streamlit as st


def _calculate_bmi(
    height,
    weight,
):
    if height <= 0:
        return None

    return weight / (
        height ** 2
    )


def _get_bmi_category(
    bmi,
    age,
):
    if age < 20:
        return {
            "label":
                "Age-specific BMI interpretation required",
            "class":
                "age-specific",
        }

    if bmi < 18.5:
        return {
            "label":
                "Underweight range",
            "class":
                "underweight",
        }

    if bmi < 25:
        return {
            "label":
                "Normal range",
            "class":
                "normal",
        }

    if bmi < 30:
        return {
            "label":
                "Overweight range",
            "class":
                "overweight",
        }

    return {
        "label":
            "Obesity range",
        "class":
            "obesity",
    }


def render_bmi_indicator(
    age,
    height,
    weight,
):
    try:
        age = float(age)
        height = float(height)
        weight = float(weight)

    except (
        TypeError,
        ValueError,
    ):
        return

    bmi = _calculate_bmi(
        height,
        weight,
    )

    if bmi is None:
        return

    category = _get_bmi_category(
        bmi,
        age,
    )

    if age < 20:
        bmi_notice_extra = """
        <br><br>

        BMI value is calculated, but
        interpretation requires
        age-specific growth references.
        """
    else:
        bmi_notice_extra = ""

    bmi_position = max(
        0,
        min(
            (
                (bmi - 10)
                / (45 - 10)
            )
            * 100,
            100,
        ),
    )

    scale_html = f"""
    <div class="health-bmi-scale">

        <div
            class="health-bmi-marker"
            style="
                left:
                {bmi_position:.1f}%;
            "
        >
        </div>

    </div>


    <div class="health-bmi-scale-labels">

        <span>
            Underweight
        </span>

        <span>
            Normal
        </span>

        <span>
            Overweight
        </span>

        <span>
            Obesity
        </span>

    </div>
    """

    st.html(
        f"""
        <section class="health-bmi-card">

            <div class="health-bmi-header">

                <div>

                    <div
                        class="health-result-eyebrow"
                    >
                        Supporting Health Indicator
                    </div>

                    <div
                        class="health-bmi-title"
                    >
                        Body Mass Index
                    </div>

                </div>

                <div
                    class="
                        health-bmi-category
                        {category["class"]}
                    "
                >
                    {category["label"]}
                </div>

            </div>


            <div class="health-bmi-value">
                {bmi:.1f}
            </div>

            <div class="health-bmi-unit">
                kg/m²
            </div>

            {scale_html}


            <div class="health-bmi-details">

                Calculated from
                <strong>
                    {height:.2f} m
                </strong>
                and
                <strong>
                    {weight:.1f} kg
                </strong>.

            </div>


            <div class="health-bmi-notice">

                BMI is shown as supporting
                information only and is not
                added to the model input by
                this interface.

                {bmi_notice_extra}

            </div>

        </section>
        """
    )