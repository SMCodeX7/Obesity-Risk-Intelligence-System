from html import escape
from io import BytesIO

from reportlab.graphics.shapes import (
    Drawing,
    Rect,
    String,
)
from reportlab.lib import colors
from reportlab.lib.enums import (
    TA_CENTER,
)
from reportlab.lib.pagesizes import (
    A4,
)
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import (
    mm,
)
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
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


FEATURE_GROUPS = {
    "Personal and Physical Information": [
        (
            "Age",
            "Age",
        ),
        (
            "Gender",
            "Gender",
        ),
        (
            "Height",
            "Height (m)",
        ),
        (
            "Weight",
            "Weight (kg)",
        ),
        (
            "family_history_with_overweight",
            "Family History of Overweight",
        ),
    ],

    "Eating Habits": [
        (
            "FCVC",
            "Vegetable Consumption (FCVC)",
        ),
        (
            "NCP",
            "Main Meals (NCP)",
        ),
        (
            "CAEC",
            "Food Between Meals (CAEC)",
        ),
        (
            "FAVC",
            "High-Calorie Food (FAVC)",
        ),
        (
            "CH2O",
            "Water Consumption (CH2O)",
        ),
        (
            "CALC",
            "Alcohol Consumption (CALC)",
        ),
    ],

    "Lifestyle and Activity": [
        (
            "FAF",
            "Physical Activity (FAF)",
        ),
        (
            "TUE",
            "Technology Use (TUE)",
        ),
        (
            "SMOKE",
            "Smoking",
        ),
        (
            "SCC",
            "Calorie Monitoring",
        ),
        (
            "MTRANS",
            "Transportation",
        ),
    ],
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


def _create_styles():
    styles = (
        getSampleStyleSheet()
    )

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            textColor=colors.HexColor(
                "#17324D"
            ),
            alignment=TA_CENTER,
            spaceAfter=5 * mm,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor(
                "#566573"
            ),
            alignment=TA_CENTER,
            spaceAfter=7 * mm,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor(
                "#17324D"
            ),
            spaceBefore=4 * mm,
            spaceAfter=3 * mm,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ResultLabel",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            textColor=colors.HexColor(
                "#5D6D7E"
            ),
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ResultValue",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=20,
            textColor=colors.HexColor(
                "#17324D"
            ),
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallText",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor(
                "#5D6D7E"
            ),
        )
    )

    styles.add(
        ParagraphStyle(
            name="Disclaimer",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=colors.HexColor(
                "#7B241C"
            ),
            backColor=colors.HexColor(
                "#FDEDEC"
            ),
            borderColor=colors.HexColor(
                "#E6B0AA"
            ),
            borderWidth=0.5,
            borderPadding=8,
            spaceBefore=5 * mm,
        )
    )

    return styles


def _build_result_summary(
    prediction,
    styles,
):
    predicted_class = (
        prediction[
            "predicted_class"
        ]
    )

    confidence = float(
        prediction[
            "confidence"
        ]
    )

    result_data = [
        [
            Paragraph(
                "MODEL-PREDICTED CATEGORY",
                styles[
                    "ResultLabel"
                ],
            ),
            Paragraph(
                "PREDICTION CONFIDENCE",
                styles[
                    "ResultLabel"
                ],
            ),
        ],
        [
            Paragraph(
                escape(
                    format_class_name(
                        predicted_class
                    )
                ),
                styles[
                    "ResultValue"
                ],
            ),
            Paragraph(
                f"{confidence * 100:.2f}%",
                styles[
                    "ResultValue"
                ],
            ),
        ],
    ]

    table = Table(
        result_data,
        colWidths=[
            82 * mm,
            82 * mm,
        ],
        rowHeights=[
            9 * mm,
            18 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor(
                        "#F4F6F7"
                    ),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    colors.HexColor(
                        "#CCD1D1"
                    ),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor(
                        "#D5DBDB"
                    ),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER",
                ),
            ]
        )
    )

    return table


def _build_input_table(
    inputs,
    feature_group,
):
    rows = [
        [
            "Feature",
            "Value",
        ]
    ]

    for feature, label in feature_group:
        value = inputs.get(
            feature,
            "Unavailable",
        )

        if isinstance(
            value,
            float,
        ):
            value = (
                f"{value:.2f}"
            )

        rows.append(
            [
                label,
                str(
                    value
                ),
            ]
        )

    table = Table(
        rows,
        colWidths=[
            105 * mm,
            59 * mm,
        ],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#17324D"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor(
                        "#D5DBDB"
                    ),
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.white,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor(
                            "#F8F9F9"
                        ),
                    ],
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    return table


def _build_probability_chart(
    probabilities,
):
    width = 470
    height = 190

    drawing = Drawing(
        width,
        height,
    )

    bar_x = 155
    bar_width = 250

    start_y = 165
    row_height = 24

    for index, class_name in enumerate(
        CLASS_ORDER
    ):
        probability = float(
            probabilities.get(
                class_name,
                0.0,
            )
        )

        y = (
            start_y
            - (
                index
                * row_height
            )
        )

        readable_name = (
            format_class_name(
                class_name
            )
        )

        drawing.add(
            String(
                0,
                y + 3,
                readable_name,
                fontName="Helvetica",
                fontSize=8,
                fillColor=(
                    colors.HexColor(
                        "#34495E"
                    )
                ),
            )
        )

        drawing.add(
            Rect(
                bar_x,
                y,
                bar_width,
                10,
                strokeColor=(
                    colors.HexColor(
                        "#D5DBDB"
                    )
                ),
                fillColor=(
                    colors.HexColor(
                        "#ECF0F1"
                    )
                ),
            )
        )

        drawing.add(
            Rect(
                bar_x,
                y,
                bar_width
                * max(
                    min(
                        probability,
                        1.0,
                    ),
                    0.0,
                ),
                10,
                strokeColor=None,
                fillColor=(
                    colors.HexColor(
                        "#2874A6"
                    )
                ),
            )
        )

        drawing.add(
            String(
                415,
                y + 3,
                f"{probability * 100:.2f}%",
                fontName=(
                    "Helvetica-Bold"
                ),
                fontSize=8,
                fillColor=(
                    colors.HexColor(
                        "#17324D"
                    )
                ),
            )
        )

    return drawing


def _build_probability_table(
    probabilities,
):
    rows = [
        [
            "Category",
            "Probability",
        ]
    ]

    sorted_probabilities = sorted(
        (
            (
                class_name,
                float(
                    probabilities.get(
                        class_name,
                        0.0,
                    )
                ),
            )
            for class_name in CLASS_ORDER
        ),
        key=lambda item:
            item[1],
        reverse=True,
    )

    for (
        class_name,
        probability,
    ) in sorted_probabilities:
        rows.append(
            [
                format_class_name(
                    class_name
                ),
                f"{probability * 100:.2f}%",
            ]
        )

    table = Table(
        rows,
        colWidths=[
            120 * mm,
            44 * mm,
        ],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#2874A6"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (1, 0),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor(
                        "#D5DBDB"
                    ),
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor(
                            "#F8F9F9"
                        ),
                    ],
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    return table


def _draw_page_footer(
    canvas,
    document,
):
    canvas.saveState()

    page_width, _ = A4

    canvas.setStrokeColor(
        colors.HexColor(
            "#D5DBDB"
        )
    )

    canvas.line(
        20 * mm,
        14 * mm,
        page_width - 20 * mm,
        14 * mm,
    )

    canvas.setFont(
        "Helvetica",
        7.5,
    )

    canvas.setFillColor(
        colors.HexColor(
            "#7F8C8D"
        )
    )

    canvas.drawString(
        20 * mm,
        9 * mm,
        (
            "Obesity Risk "
            "Intelligence System"
        ),
    )

    canvas.drawRightString(
        page_width - 20 * mm,
        9 * mm,
        f"Page {document.page}",
    )

    canvas.restoreState()


def generate_prediction_report(
    prediction,
):
    buffer = BytesIO()

    document = (
        SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=18 * mm,
            bottomMargin=20 * mm,
            title=(
                "Obesity Risk "
                "Assessment Report"
            ),
            author=(
                "Obesity Risk "
                "Intelligence System"
            ),
        )
    )

    styles = (
        _create_styles()
    )

    story = []

    created_at = (
        format_sri_lanka_datetime(
            prediction.get(
                "created_at"
            )
        )
    )

    story.append(
        Paragraph(
            (
                "Obesity Risk "
                "Intelligence System"
            ),
            styles[
                "ReportTitle"
            ],
        )
    )

    story.append(
        Paragraph(
            (
                "Machine Learning "
                "Assessment Report"
            ),
            styles[
                "ReportSubtitle"
            ],
        )
    )

    report_information = Table(
        [
            [
                "Assessment Date",
                str(
                    created_at
                ),
            ]
        ],
        colWidths=[
            42 * mm,
            122 * mm,
        ],
    )

    report_information.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor(
                        "#F4F6F7"
                    ),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8.5,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor(
                        "#D5DBDB"
                    ),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(
        report_information
    )

    story.append(
        Spacer(
            1,
            6 * mm,
        )
    )

    story.append(
        Paragraph(
            "Assessment Result",
            styles[
                "SectionHeading"
            ],
        )
    )

    story.append(
        _build_result_summary(
            prediction,
            styles,
        )
    )

    story.append(
        Spacer(
            1,
            5 * mm,
        )
    )

    inputs = (
        prediction.get(
            "inputs",
            {},
        )
    )

    for (
        section_name,
        feature_group,
    ) in FEATURE_GROUPS.items():

        section = [
            Paragraph(
                escape(
                    section_name
                ),
                styles[
                    "SectionHeading"
                ],
            ),
            _build_input_table(
                inputs,
                feature_group,
            ),
        ]

        story.append(
            KeepTogether(
                section
            )
        )

    story.append(
        Paragraph(
            (
                "Class Probability "
                "Distribution"
            ),
            styles[
                "SectionHeading"
            ],
        )
    )

    probabilities = (
        prediction.get(
            "probabilities",
            {},
        )
    )

    story.append(
        _build_probability_chart(
            probabilities
        )
    )

    story.append(
        Spacer(
            1,
            3 * mm,
        )
    )

    story.append(
        _build_probability_table(
            probabilities
        )
    )

    story.append(
        Paragraph(
            "Model Information",
            styles[
                "SectionHeading"
            ],
        )
    )

    model_table = Table(
        [
            [
                "Model",
                str(
                    prediction.get(
                        "model_name",
                        "Unavailable",
                    )
                ),
            ],
            [
                "Scikit-learn Version",
                str(
                    prediction.get(
                        "scikit_learn_version",
                        "Unavailable",
                    )
                ),
            ],
        ],
        colWidths=[
            55 * mm,
            109 * mm,
        ],
    )

    model_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor(
                        "#F4F6F7"
                    ),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    colors.HexColor(
                        "#D5DBDB"
                    ),
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    story.append(
        model_table
    )

    story.append(
        Paragraph(
            (
                "<b>Important Notice:</b> "
                "This report was generated "
                "by an educational machine "
                "learning system. The result "
                "is not a medical diagnosis, "
                "does not establish medical "
                "certainty, and should not "
                "replace evaluation or advice "
                "from a qualified healthcare "
                "professional."
            ),
            styles[
                "Disclaimer"
            ],
        )
    )

    document.build(
        story,
        onFirstPage=(
            _draw_page_footer
        ),
        onLaterPages=(
            _draw_page_footer
        ),
    )

    pdf_bytes = (
        buffer.getvalue()
    )

    buffer.close()

    return pdf_bytes