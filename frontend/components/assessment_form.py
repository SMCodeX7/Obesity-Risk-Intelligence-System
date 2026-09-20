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
    1: "Personal Information",
    2: "Nutrition Habits",
    3: "Lifestyle Factors",
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
    steps_data = [
        (1, "Personal Information", "👤", "Age, gender & measurements"),
        (2, "Nutrition Habits", "🥗", "Eating behaviour & hydration"),
        (3, "Lifestyle Factors", "🏃", "Physical activity & habits"),
    ]

    current_name = STEP_NAMES.get(
        current_step,
        "Personal Information",
    )
    progress_percent = int(
        (current_step / 3) * 100
    )

    cards_html = []
    for (
        step_num,
        step_name,
        icon,
        step_desc,
    ) in steps_data:
        if step_num < current_step:
            state_class = "complete"
            status_badge = '<span class="health-step-badge done">✓ Completed</span>'
            circle_content = "✓"
        elif step_num == current_step:
            state_class = "active"
            status_badge = '<span class="health-step-badge current">● In Progress</span>'
            circle_content = str(step_num)
        else:
            state_class = "upcoming"
            status_badge = '<span class="health-step-badge pending">○ Upcoming</span>'
            circle_content = str(step_num)

        cards_html.append(
            f"""
            <div class="health-step-card {state_class}">
                <div class="health-step-card-header">
                    <div class="health-step-number-circle">{circle_content}</div>
                    {status_badge}
                </div>
                <div class="health-step-card-title">{icon} {step_name}</div>
                <div class="health-step-card-desc">{step_desc}</div>
            </div>
            """
        )

    dot_1_state = "complete" if current_step > 1 else ("active" if current_step == 1 else "pending")
    dot_1_icon = "✓" if current_step > 1 else "●"

    dot_2_state = "complete" if current_step > 2 else ("active" if current_step == 2 else "pending")
    dot_2_icon = "✓" if current_step > 2 else ("●" if current_step == 2 else "○")

    dot_3_state = "active" if current_step == 3 else "pending"
    dot_3_icon = "●" if current_step == 3 else "○"

    stepper_html = f"""
    <div class="health-stepper-container">
        <!-- Progress Indicator Panel: Step X of 3 / Title / ━━━━━━○○○ style -->
        <div class="health-progress-panel">
            <div class="health-progress-row">
                <div class="health-progress-meta">
                    <span class="health-progress-step-pill">Step {current_step} of 3</span>
                    <h3 class="health-progress-title">{current_name}</h3>
                </div>
                <div class="health-progress-pct-badge">{progress_percent}% Complete</div>
            </div>
            <div class="health-progress-visual">
                <div class="health-progress-bar-track">
                    <div class="health-progress-bar-fill step-{current_step}"></div>
                </div>
                <div class="health-progress-dots-row">
                    <div class="health-dot-node {dot_1_state}">
                        <span class="health-dot-circle">{dot_1_icon}</span>
                        <span class="health-dot-label">1. Personal Information</span>
                    </div>
                    <div class="health-dot-node {dot_2_state}">
                        <span class="health-dot-circle">{dot_2_icon}</span>
                        <span class="health-dot-label">2. Nutrition Habits</span>
                    </div>
                    <div class="health-dot-node {dot_3_state}">
                        <span class="health-dot-circle">{dot_3_icon}</span>
                        <span class="health-dot-label">3. Lifestyle Factors</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3 Step Cards Grid -->
        <div class="health-stepper-cards">
            {"".join(cards_html)}
        </div>
    </div>
    """

    st.html(stepper_html)


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
            <div class="health-info-content">
                <div class="health-info-title">
                    {title}
                </div>
                <div class="health-info-text">
                    {description}
                </div>
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
            "Personal Information & Body Measurements"
        ),
        description=(
            "Enter demographic characteristics and anthropometric measurements. "
            "These inputs establish the metabolic baseline for the machine learning risk model."
        ),
    )

    with st.form(
        "assessment_profile_form"
    ):
        # Section 1: Personal Information
        with st.container(
            border=True
        ):
            st.html(
                """
                <div class="health-section-header health-section-header--blue">
                    <div class="health-section-icon-wrap health-section-icon-wrap--blue">👤</div>
                    <div class="health-section-text-wrap">
                        <div class="health-section-meta-row">
                            <span class="health-section-kicker health-section-kicker--blue">Section 1 · Profile</span>
                            <span class="health-section-badge health-section-badge--blue">Demographics</span>
                        </div>
                        <h4 class="health-section-title">Personal Information</h4>
                        <div class="health-section-subtitle">Demographic characteristics, biological sex, and genetic predisposition</div>
                    </div>
                </div>
                """
            )

            col1, col2 = (
                st.columns(
                    2,
                    gap="large",
                )
            )

            with col1:
                age = st.number_input(
                    "Age",
                    min_value=1.0,
                    max_value=120.0,
                    value=float(
                        data["Age"]
                    ),
                    step=1.0,
                    key="input_age",
                    help="Enter age in years.",
                )

            with col2:
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
                    help="Select biological sex category used in clinical model training.",
                )

            col3, col4 = (
                st.columns(
                    2,
                    gap="large",
                )
            )

            with col3:
                family_options = [
                    "yes",
                    "no",
                ]

                family_history = (
                    st.selectbox(
                        (
                            "Family history of overweight"
                        ),
                        options=family_options,
                        index=_option_index(
                            family_options,
                            data[
                                "family_history_with_overweight"
                            ],
                        ),
                        key="input_family_history",
                        format_func=lambda value: (
                            "Yes"
                            if value == "yes"
                            else "No"
                        ),
                        help="Indicates whether overweight has occurred within the family.",
                    )
                )

            with col4:
                st.html(
                    """
                    <div class="health-field-hint">
                        <div class="health-hint-badge">Genetic Factor</div>
                        <div class="health-hint-desc">Family medical history accounts for hereditary metabolic traits and shared lifestyle patterns.</div>
                    </div>
                    """
                )

        # Section 2: Body Measurements
        with st.container(
            border=True
        ):
            st.html(
                """
                <div class="health-section-header health-section-header--indigo">
                    <div class="health-section-icon-wrap health-section-icon-wrap--indigo">⚖️</div>
                    <div class="health-section-text-wrap">
                        <div class="health-section-meta-row">
                            <span class="health-section-kicker health-section-kicker--indigo">Section 2 · Anthropometry</span>
                            <span class="health-section-badge health-section-badge--indigo">Biometrics</span>
                        </div>
                        <h4 class="health-section-title">Body Measurements</h4>
                        <div class="health-section-subtitle">Height and weight to determine Body Mass Index (BMI) and physical dimensions</div>
                    </div>
                </div>
                """
            )

            m_col1, m_col2 = (
                st.columns(
                    2,
                    gap="large",
                )
            )

            with m_col1:
                height = st.number_input(
                    "Height (metres)",
                    min_value=0.50,
                    max_value=2.50,
                    value=float(
                        data["Height"]
                    ),
                    step=0.01,
                    format="%.2f",
                    key="input_height",
                    help="Enter height in metres. Example: 1.70 m.",
                )

            with m_col2:
                weight = st.number_input(
                    "Weight (kg)",
                    min_value=10.0,
                    max_value=350.0,
                    value=float(
                        data["Weight"]
                    ),
                    step=0.5,
                    format="%.1f",
                    key="input_weight",
                    help="Enter weight in kilograms.",
                )

        st.html(
            """
            <div class="health-notice">
                <div class="health-notice-icon">💡</div>
                <div class="health-notice-body">
                    <strong>Why these metrics matter</strong>
                    <p>Age, gender, height, weight, and family history form the foundational anthropometric baseline of the 16 clinical signals analyzed by the model.</p>
                </div>
            </div>
            """
        )

        st.write("")

        submitted = (
            st.form_submit_button(
                "Continue to Nutrition Habits →",
                type="primary",
                width="stretch",
            )
        )

    if submitted:
        update_assessment_data(
            {
                "Age": float(age),
                "Height": float(height),
                "Weight": float(weight),
                "Gender": gender,
                "family_history_with_overweight": family_history,
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
        title="Nutrition Habits & Dietary Factors",
        description=(
            "Describe typical eating and hydration patterns. Technical dataset "
            "variables are calibrated to everyday lifestyle choices."
        ),
    )

    with st.form(
        "assessment_nutrition_form"
    ):
        # Eating Behaviour Card
        with st.container(
            border=True
        ):
            st.html(
                """
                <div class="health-section-header health-section-header--green">
                    <div class="health-section-icon-wrap health-section-icon-wrap--green">🥗</div>
                    <div class="health-section-text-wrap">
                        <div class="health-section-meta-row">
                            <span class="health-section-kicker health-section-kicker--green">Dietary Patterns</span>
                            <span class="health-section-badge health-section-badge--green">Nutrition</span>
                        </div>
                        <h4 class="health-section-title">Eating Behaviour</h4>
                        <div class="health-section-subtitle">Meal frequency, vegetable consumption, snacking, and high-calorie food intake</div>
                    </div>
                </div>
                """
            )

            left, right = (
                st.columns(
                    2,
                    gap="large",
                )
            )

            with left:
                fcvc = st.slider(
                    (
                        "Vegetable consumption score"
                    ),
                    min_value=1.0,
                    max_value=3.0,
                    value=float(
                        data["FCVC"]
                    ),
                    step=0.1,
                    key="input_fcvc",
                    help=(
                        "Model feature FCVC. Scale ranges from 1 (rarely) to 3 (always)."
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
                        "Model feature NCP. Number of main meals per day (1 to 4)."
                    ),
                )

            with right:
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
                    format_func=lambda value: (
                        "No"
                        if value == "no"
                        else value
                    ),
                    help=(
                        "How frequently food is consumed between main meals."
                    ),
                )

                favc_options = [
                    "yes",
                    "no",
                ]

                favc = st.selectbox(
                    (
                        "Frequent high-calorie food consumption"
                    ),
                    options=favc_options,
                    index=_option_index(
                        favc_options,
                        data["FAVC"],
                    ),
                    key="input_favc",
                    format_func=lambda value: (
                        "Yes"
                        if value == "yes"
                        else "No"
                    ),
                    help=(
                        "Whether high-calorie or processed foods are consumed frequently."
                    ),
                )

        # Hydration & Intake Card
        with st.container(
            border=True
        ):
            st.html(
                """
                <div class="health-section-header health-section-header--cyan">
                    <div class="health-section-icon-wrap health-section-icon-wrap--cyan">💧</div>
                    <div class="health-section-text-wrap">
                        <div class="health-section-meta-row">
                            <span class="health-section-kicker health-section-kicker--cyan">Intake & Hydration</span>
                            <span class="health-section-badge health-section-badge--cyan">Fluid Balance</span>
                        </div>
                        <h4 class="health-section-title">Hydration & Alcohol Intake</h4>
                        <div class="health-section-subtitle">Daily water consumption levels and alcohol intake frequency</div>
                    </div>
                </div>
                """
            )

            h_left, h_right = (
                st.columns(
                    2,
                    gap="large",
                )
            )

            with h_left:
                ch2o = st.slider(
                    (
                        "Daily water consumption score"
                    ),
                    min_value=1.0,
                    max_value=3.0,
                    value=float(
                        data["CH2O"]
                    ),
                    step=0.1,
                    key="input_ch2o",
                    help=(
                        "Model feature CH2O. Daily hydration scale (1: <1L, 2: 1-2L, 3: >2L)."
                    ),
                )

            with h_right:
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
                    format_func=lambda value: (
                        "No"
                        if value == "no"
                        else value
                    ),
                    help=(
                        "Frequency of alcohol consumption represented by model feature CALC."
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
                        "Continue to Lifestyle Factors →"
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
                "FCVC": float(fcvc),
                "NCP": float(ncp),
                "CAEC": caec,
                "FAVC": favc,
                "CH2O": float(ch2o),
                "CALC": calc,
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
        title="Lifestyle Factors & Daily Habits",
        description=(
            "Complete the assessment with physical activity, screen time, "
            "tobacco use, calorie tracking, and daily transportation habits."
        ),
    )

    with st.form(
        "assessment_lifestyle_form"
    ):
        # Section 3: Activity & Technology
        with st.container(
            border=True
        ):
            st.html(
                """
                <div class="health-section-header health-section-header--orange">
                    <div class="health-section-icon-wrap health-section-icon-wrap--orange">🏃</div>
                    <div class="health-section-text-wrap">
                        <div class="health-section-meta-row">
                            <span class="health-section-kicker health-section-kicker--orange">Section 3 · Activity & Screen Time</span>
                            <span class="health-section-badge health-section-badge--orange">Physical Movement</span>
                        </div>
                        <h4 class="health-section-title">Physical Activity & Technology Usage</h4>
                        <div class="health-section-subtitle">Weekly exercise frequency and daily screen time metrics</div>
                    </div>
                </div>
                """
            )

            left, right = (
                st.columns(
                    2,
                    gap="large",
                )
            )

            with left:
                faf = st.slider(
                    (
                        "Physical activity score"
                    ),
                    min_value=0.0,
                    max_value=3.0,
                    value=float(
                        data["FAF"]
                    ),
                    step=0.1,
                    key="input_faf",
                    help=(
                        "Model feature FAF. Physical activity frequency (0: none, 3: high)."
                    ),
                )

            with right:
                tue = st.slider(
                    (
                        "Technology usage score"
                    ),
                    min_value=0.0,
                    max_value=2.0,
                    value=float(
                        data["TUE"]
                    ),
                    step=0.1,
                    key="input_tue",
                    help=(
                        "Model feature TUE. Daily hours spent on electronic devices (0 to 2)."
                    ),
                )

        # Section 3: Daily Habits & Mobility
        with st.container(
            border=True
        ):
            st.html(
                """
                <div class="health-section-header health-section-header--orange">
                    <div class="health-section-icon-wrap health-section-icon-wrap--orange">🚲</div>
                    <div class="health-section-text-wrap">
                        <div class="health-section-meta-row">
                            <span class="health-section-kicker health-section-kicker--orange">Section 3 · Daily Habits & Mobility</span>
                            <span class="health-section-badge health-section-badge--orange">Transit & Habits</span>
                        </div>
                        <h4 class="health-section-title">Daily Habits & Transportation</h4>
                        <div class="health-section-subtitle">Tobacco exposure, active calorie monitoring, and transit method</div>
                    </div>
                </div>
                """
            )

            col1, col2, col3 = (
                st.columns(
                    3,
                    gap="medium",
                )
            )

            with col1:
                smoke_options = [
                    "no",
                    "yes",
                ]

                smoke = st.selectbox(
                    "Smoking status",
                    options=smoke_options,
                    index=_option_index(
                        smoke_options,
                        data["SMOKE"],
                    ),
                    key="input_smoke",
                    format_func=lambda value: (
                        "No"
                        if value == "no"
                        else "Yes"
                    ),
                    help="Indicates active tobacco smoking.",
                )

            with col2:
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
                    format_func=lambda value: (
                        "No"
                        if value == "no"
                        else "Yes"
                    ),
                    help=(
                        "Whether daily calorie consumption is actively tracked."
                    ),
                )

            with col3:
                transport_options = [
                    "Public_Transportation",
                    "Automobile",
                    "Walking",
                    "Motorbike",
                    "Bike",
                ]

                mtrans = st.selectbox(
                    (
                        "Primary transportation"
                    ),
                    options=(
                        transport_options
                    ),
                    index=_option_index(
                        transport_options,
                        data["MTRANS"],
                    ),
                    key="input_mtrans",
                    format_func=lambda value: (
                        value.replace(
                            "_",
                            " ",
                        )
                    ),
                    help="Primary commuting method for physical exertion calculation.",
                )

        st.html(
            """
            <div class="health-notice ready-notice">
                <div class="health-notice-icon">✨</div>
                <div class="health-notice-body">
                    <strong>Ready for Machine Learning Analysis</strong>
                    <p>Your complete profile will be analyzed across 16 clinically validated signals to generate an instant risk classification, confidence metric, and full probability distribution.</p>
                </div>
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
                    "Run Risk Assessment 🚀",
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
                "FAF": float(faf),
                "TUE": float(tue),
                "SMOKE": smoke,
                "SCC": scc,
                "MTRANS": mtrans,
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