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



    # Build per-segment reference rows (value ranges fixed — no logic change)
    ranges = [
        ("Underweight", "&lt; 18.5", "underweight"),
        ("Normal weight", "18.5 – 24.9", "normal"),
        ("Overweight", "25 – 29.9", "overweight"),
        ("Obesity", "≥ 30", "obesity"),
    ]
    ranges_html = "".join(
        f'<div class="health-bmi-ref-row bmi-ref-{r[2]}">'
        f'<span class="health-bmi-ref-label">{r[0]}</span>'
        f'<span class="health-bmi-ref-range">{r[1]}</span>'
        f'</div>'
        for r in ranges
    )

    st.html(
        f"""
        <section class="health-bmi-card">

            <!-- ── Header ── -->
            <div class="health-bmi-header">
                <div class="health-bmi-header-left">
                    <span class="health-bmi-kicker">Body Mass Index</span>
                    <div class="health-bmi-hero-row">
                        <span class="health-bmi-value">{bmi:.1f}</span>
                        <span class="health-bmi-unit">kg/m²</span>
                        <span class="health-bmi-badge {category["class"]}">
                            {category["label"]}
                        </span>
                    </div>
                    <div class="health-bmi-inputs">
                        Height&nbsp;<strong>{height:.2f}&thinsp;m</strong>
                        &nbsp;·&nbsp;
                        Weight&nbsp;<strong>{weight:.1f}&thinsp;kg</strong>
                    </div>
                </div>
                <div class="health-bmi-ref-table">
                    {ranges_html}
                </div>
            </div>

            <!-- ── Scale ── -->
            <div class="health-bmi-scale-wrap">
                <div class="health-bmi-scale">
                    <div class="health-bmi-marker" style="left:{bmi_position:.1f}%;">
                        <div class="health-bmi-marker-tip"></div>
                    </div>
                    <div class="health-bmi-seg seg-underweight"></div>
                    <div class="health-bmi-seg seg-normal"></div>
                    <div class="health-bmi-seg seg-overweight"></div>
                    <div class="health-bmi-seg seg-obesity"></div>
                </div>
                <div class="health-bmi-scale-labels">
                    <span>10</span>
                    <span>18.5</span>
                    <span>25</span>
                    <span>30</span>
                    <span>45</span>
                </div>
            </div>

            <!-- ── Footer notice ── -->
            <div class="health-bmi-notice">
                <span class="health-bmi-notice-icon">ⓘ</span>
                BMI is shown as supporting information only — it is not passed to the
                classification model.{bmi_notice_extra}
            </div>

        </section>
        """
    )