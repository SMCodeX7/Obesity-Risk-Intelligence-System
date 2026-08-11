import streamlit as st


FORM_WIDGET_KEYS = [
    "input_age",
    "input_height",
    "input_weight",
    "input_gender",
    "input_family_history",
    "input_fcvc",
    "input_ncp",
    "input_caec",
    "input_favc",
    "input_ch2o",
    "input_calc",
    "input_faf",
    "input_tue",
    "input_smoke",
    "input_scc",
    "input_mtrans",
]


STEP_NAMES = {
    1: "Profile",
    2: "Nutrition",
    3: "Lifestyle",
}


DEFAULT_ASSESSMENT_DATA = {
    "Age": 25.0,
    "Height": 1.70,
    "Weight": 70.0,
    "FCVC": 2.0,
    "NCP": 3.0,
    "CH2O": 2.0,
    "FAF": 1.0,
    "TUE": 1.0,
    "CAEC": "no",
    "CALC": "no",
    "Gender": "Female",
    "family_history_with_overweight": "yes",
    "FAVC": "yes",
    "SMOKE": "no",
    "SCC": "no",
    "MTRANS": "Public_Transportation",
}


def initialize_assessment_data():
    if (
        "assessment_data"
        not in st.session_state
    ):
        st.session_state[
            "assessment_data"
        ] = (
            DEFAULT_ASSESSMENT_DATA.copy()
        )


def get_assessment_data():
    initialize_assessment_data()

    return st.session_state[
        "assessment_data"
    ]


def update_assessment_data(
    values,
):
    current_data = (
        get_assessment_data().copy()
    )

    current_data.update(
        values
    )

    st.session_state[
        "assessment_data"
    ] = current_data


def reset_assessment_form():
    for key in FORM_WIDGET_KEYS:
        st.session_state.pop(
            key,
            None,
        )

    st.session_state.pop(
        "assessment_data",
        None,
    )

    st.session_state[
        "assessment_step"
    ] = 1

    st.session_state[
        "prediction_result"
    ] = None


def build_assessment_payload(
    data,
):
    return {
        "Age":
            float(
                data[
                    "Age"
                ]
            ),

        "Height":
            float(
                data[
                    "Height"
                ]
            ),

        "Weight":
            float(
                data[
                    "Weight"
                ]
            ),

        "FCVC":
            float(
                data[
                    "FCVC"
                ]
            ),

        "NCP":
            float(
                data[
                    "NCP"
                ]
            ),

        "CH2O":
            float(
                data[
                    "CH2O"
                ]
            ),

        "FAF":
            float(
                data[
                    "FAF"
                ]
            ),

        "TUE":
            float(
                data[
                    "TUE"
                ]
            ),

        "CAEC":
            data[
                "CAEC"
            ],

        "CALC":
            data[
                "CALC"
            ],

        "Gender":
            data[
                "Gender"
            ],

        "family_history_with_overweight":
            data[
                "family_history_with_overweight"
            ],

        "FAVC":
            data[
                "FAVC"
            ],

        "SMOKE":
            data[
                "SMOKE"
            ],

        "SCC":
            data[
                "SCC"
            ],

        "MTRANS":
            data[
                "MTRANS"
            ],
    }


def _option_index(
    options,
    value,
):
    try:
        return options.index(
            value
        )

    except ValueError:
        return 0


def _render_stepper(
    current_step,
):
    step_html = []

    for (
        step_number,
        step_name,
    ) in STEP_NAMES.items():

        if (
            step_number
            < current_step
        ):
            state_class = (
                "complete"
            )

            display_number = "✓"

        elif (
            step_number
            == current_step
        ):
            state_class = (
                "active"
            )

            display_number = str(
                step_number
            )

        else:
            state_class = ""

            display_number = str(
                step_number
            )

        step_html.append(
            f"""
            <div
                class="
                    health-step
                    {state_class}
                "
            >

                <div
                    class="
                        health-step-number
                    "
                >
                    {display_number}
                </div>

                <div
                    class="
                        health-step-name
                    "
                >
                    {step_name}
                </div>

            </div>
            """
        )

    st.html(
        (
            '<div class="health-stepper">'
            + "".join(
                step_html
            )
            + "</div>"
        )
    )


def _render_step_information(
    number,
    title,
    description,
):
    st.html(
        f"""
        <div class="health-info-card">

            <div class="health-info-icon">
                {number:02d}
            </div>

            <div class="health-info-title">
                {title}
            </div>

            <div class="health-info-text">
                {description}
            </div>

        </div>
        """
    )


def _render_profile_step():
    data = (
        get_assessment_data()
    )

    _render_step_information(
        number=1,
        title=(
            "Personal and physical "
            "profile"
        ),
        description=(
            "Start with basic physical "
            "and demographic information. "
            "These values form the first "
            "part of the machine learning "
            "risk profile."
        ),
    )

    with st.form(
        "assessment_profile_form"
    ):

        left, right = (
            st.columns(
                2,
                gap="large",
            )
        )

        with left:

            age = st.number_input(
                "Age",
                min_value=1.0,
                max_value=120.0,
                value=float(
                    data["Age"]
                ),
                step=1.0,
                key="input_age",
                help=(
                    "Enter age in years."
                ),
            )

            height = st.number_input(
                "Height",
                min_value=0.50,
                max_value=2.50,
                value=float(
                    data["Height"]
                ),
                step=0.01,
                format="%.2f",
                key="input_height",
                help=(
                    "Enter height in metres. "
                    "Example: 1.70 m."
                ),
            )

            weight = st.number_input(
                "Weight",
                min_value=10.0,
                max_value=350.0,
                value=float(
                    data["Weight"]
                ),
                step=0.5,
                format="%.1f",
                key="input_weight",
                help=(
                    "Enter weight in kilograms."
                ),
            )

        with right:

            gender_options = [
                "Female",
                "Male",
            ]

            gender = st.selectbox(
                "Gender",
                options=gender_options,
                index=_option_index(
                    gender_options,
                    data["Gender"],
                ),
                key="input_gender",
                help=(
                    "Select the category "
                    "used by the training "
                    "dataset."
                ),
            )

            family_options = [
                "yes",
                "no",
            ]

            family_history = (
                st.selectbox(
                    (
                        "Family history "
                        "of overweight"
                    ),
                    options=(
                        family_options
                    ),
                    index=_option_index(
                        family_options,
                        data[
                            "family_history_with_overweight"
                        ],
                    ),
                    key=(
                        "input_family_history"
                    ),
                    format_func=lambda value:
                        (
                            "Yes"
                            if value == "yes"
                            else "No"
                        ),
                    help=(
                        "Indicates whether "
                        "overweight has occurred "
                        "within the family."
                    ),
                )
            )

            st.html(
                """
                <div class="health-notice">

                    <strong>
                        Why these details?
                    </strong>

                    <br><br>

                    Age, height, weight,
                    gender, and family history
                    are part of the 16 signals
                    used by the trained model.

                </div>
                """
            )

        st.write("")

        submitted = (
            st.form_submit_button(
                (
                    "Continue to Nutrition →"
                ),
                type="primary",
                width="stretch",
            )
        )

    if submitted:

        update_assessment_data(
            {
                "Age":
                    float(
                        age
                    ),

                "Height":
                    float(
                        height
                    ),

                "Weight":
                    float(
                        weight
                    ),

                "Gender":
                    gender,

                "family_history_with_overweight":
                    family_history,
            }
        )

        st.session_state[
            "assessment_step"
        ] = 2

        st.rerun()


def _render_nutrition_step():
    data = (
        get_assessment_data()
    )

    _render_step_information(
        number=2,
        title="Nutrition habits",
        description=(
            "Describe common eating and "
            "hydration patterns. Technical "
            "dataset variables are presented "
            "using clearer user-facing labels."
        ),
    )

    with st.form(
        "assessment_nutrition_form"
    ):

        left, right = (
            st.columns(
                2,
                gap="large",
            )
        )

        with left:

            fcvc = st.slider(
                (
                    "Vegetable consumption "
                    "score"
                ),
                min_value=1.0,
                max_value=3.0,
                value=float(
                    data["FCVC"]
                ),
                step=0.1,
                key="input_fcvc",
                help=(
                    "Model feature FCVC. "
                    "Scale ranges from "
                    "1 to 3."
                ),
            )

            ncp = st.slider(
                "Main meal score",
                min_value=1.0,
                max_value=4.0,
                value=float(
                    data["NCP"]
                ),
                step=0.1,
                key="input_ncp",
                help=(
                    "Model feature NCP. "
                    "Scale ranges from "
                    "1 to 4."
                ),
            )

            caec_options = [
                "no",
                "Sometimes",
                "Frequently",
                "Always",
            ]

            caec = st.selectbox(
                "Food between meals",
                options=caec_options,
                index=_option_index(
                    caec_options,
                    data["CAEC"],
                ),
                key="input_caec",
                format_func=lambda value:
                    (
                        "No"
                        if value == "no"
                        else value
                    ),
                help=(
                    "How frequently food "
                    "is consumed between "
                    "main meals."
                ),
            )

        with right:

            favc_options = [
                "yes",
                "no",
            ]

            favc = st.selectbox(
                (
                    "Frequent high-calorie "
                    "food consumption"
                ),
                options=favc_options,
                index=_option_index(
                    favc_options,
                    data["FAVC"],
                ),
                key="input_favc",
                format_func=lambda value:
                    (
                        "Yes"
                        if value == "yes"
                        else "No"
                    ),
                help=(
                    "Whether high-calorie "
                    "foods are consumed "
                    "frequently."
                ),
            )

            ch2o = st.slider(
                (
                    "Water consumption "
                    "score"
                ),
                min_value=1.0,
                max_value=3.0,
                value=float(
                    data["CH2O"]
                ),
                step=0.1,
                key="input_ch2o",
                help=(
                    "Model feature CH2O. "
                    "Scale ranges from "
                    "1 to 3."
                ),
            )

            calc_options = [
                "no",
                "Sometimes",
                "Frequently",
            ]

            calc = st.selectbox(
                "Alcohol consumption",
                options=calc_options,
                index=_option_index(
                    calc_options,
                    data["CALC"],
                ),
                key="input_calc",
                format_func=lambda value:
                    (
                        "No"
                        if value == "no"
                        else value
                    ),
                help=(
                    "Frequency of alcohol "
                    "consumption represented "
                    "by the model feature CALC."
                ),
            )

        st.write("")

        navigation_left, (
            navigation_right
        ) = st.columns(
            2,
            gap="medium",
        )

        with navigation_left:

            back_button = (
                st.form_submit_button(
                    "← Back to Profile",
                    width="stretch",
                )
            )

        with navigation_right:

            continue_button = (
                st.form_submit_button(
                    (
                        "Continue to "
                        "Lifestyle →"
                    ),
                    type="primary",
                    width="stretch",
                )
            )

    if (
        back_button
        or continue_button
    ):

        update_assessment_data(
            {
                "FCVC":
                    float(
                        fcvc
                    ),

                "NCP":
                    float(
                        ncp
                    ),

                "CAEC":
                    caec,

                "FAVC":
                    favc,

                "CH2O":
                    float(
                        ch2o
                    ),

                "CALC":
                    calc,
            }
        )

    if back_button:

        st.session_state[
            "assessment_step"
        ] = 1

        st.rerun()

    if continue_button:

        st.session_state[
            "assessment_step"
        ] = 3

        st.rerun()


def _render_lifestyle_step():
    data = (
        get_assessment_data()
    )

    _render_step_information(
        number=3,
        title=(
            "Lifestyle and activity"
        ),
        description=(
            "Complete the assessment with "
            "physical activity, technology "
            "use, smoking, calorie monitoring, "
            "and transportation patterns."
        ),
    )

    with st.form(
        "assessment_lifestyle_form"
    ):

        left, right = (
            st.columns(
                2,
                gap="large",
            )
        )

        with left:

            faf = st.slider(
                (
                    "Physical activity "
                    "score"
                ),
                min_value=0.0,
                max_value=3.0,
                value=float(
                    data["FAF"]
                ),
                step=0.1,
                key="input_faf",
                help=(
                    "Model feature FAF. "
                    "Scale ranges from "
                    "0 to 3."
                ),
            )

            tue = st.slider(
                (
                    "Technology use "
                    "score"
                ),
                min_value=0.0,
                max_value=2.0,
                value=float(
                    data["TUE"]
                ),
                step=0.1,
                key="input_tue",
                help=(
                    "Model feature TUE. "
                    "Scale ranges from "
                    "0 to 2."
                ),
            )

            smoke_options = [
                "no",
                "yes",
            ]

            smoke = st.selectbox(
                "Smoking",
                options=smoke_options,
                index=_option_index(
                    smoke_options,
                    data["SMOKE"],
                ),
                key="input_smoke",
                format_func=lambda value:
                    (
                        "No"
                        if value == "no"
                        else "Yes"
                    ),
            )

        with right:

            scc_options = [
                "no",
                "yes",
            ]

            scc = st.selectbox(
                "Calorie monitoring",
                options=scc_options,
                index=_option_index(
                    scc_options,
                    data["SCC"],
                ),
                key="input_scc",
                format_func=lambda value:
                    (
                        "No"
                        if value == "no"
                        else "Yes"
                    ),
                help=(
                    "Whether calorie "
                    "consumption is actively "
                    "monitored."
                ),
            )

            transport_options = [
                "Public_Transportation",
                "Automobile",
                "Walking",
                "Motorbike",
                "Bike",
            ]

            mtrans = st.selectbox(
                (
                    "Primary mode of "
                    "transportation"
                ),
                options=(
                    transport_options
                ),
                index=_option_index(
                    transport_options,
                    data["MTRANS"],
                ),
                key="input_mtrans",
                format_func=lambda value:
                    value.replace(
                        "_",
                        " ",
                    ),
            )

            st.html(
                """
                <div class="health-notice">

                    <strong>
                        Ready for analysis
                    </strong>

                    <br><br>

                    Your assessment will be
                    processed by the saved
                    machine learning pipeline.

                    The result is educational
                    and should not be treated
                    as a medical diagnosis.

                </div>
                """
            )

        st.write("")

        navigation_left, (
            navigation_right
        ) = st.columns(
            2,
            gap="medium",
        )

        with navigation_left:

            back_button = (
                st.form_submit_button(
                    "← Back to Nutrition",
                    width="stretch",
                )
            )

        with navigation_right:

            submit_button = (
                st.form_submit_button(
                    "Run Risk Assessment",
                    type="primary",
                    width="stretch",
                )
            )

    if (
        back_button
        or submit_button
    ):

        update_assessment_data(
            {
                "FAF":
                    float(
                        faf
                    ),

                "TUE":
                    float(
                        tue
                    ),

                "SMOKE":
                    smoke,

                "SCC":
                    scc,

                "MTRANS":
                    mtrans,
            }
        )

    if back_button:

        st.session_state[
            "assessment_step"
        ] = 2

        st.rerun()

    if submit_button:

        return (
            build_assessment_payload(
                get_assessment_data()
            )
        )

    return None


def render_assessment_form():
    is_new_assessment_state = (
        "assessment_data"
        not in st.session_state
    )

    initialize_assessment_data()

    if (
        "assessment_step"
        not in st.session_state
        or is_new_assessment_state
    ):
        st.session_state[
            "assessment_step"
        ] = 1

    current_step = (
        st.session_state[
            "assessment_step"
        ]
    )

    if current_step not in (
        1,
        2,
        3,
    ):
        current_step = 1

        st.session_state[
            "assessment_step"
        ] = 1

    _render_stepper(
        current_step
    )

    if current_step == 1:

        _render_profile_step()

        return None

    if current_step == 2:

        _render_nutrition_step()

        return None

    return (
        _render_lifestyle_step()
    )