import streamlit as st


def render_assessment_form():
    st.subheader(
        "Obesity Risk Assessment"
    )

    st.write(
        "Enter the information below "
        "to generate an obesity-risk prediction"
    )

    with st.form(
        "obesity_assessment_form"
    ):
        st.markdown(
            "### Personal and Physical Information"
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:
            age = st.number_input(
                "Age",
                min_value=1.0,
                max_value=120.0,
                value=25.0,
                step=1.0,
            )

        with col2:
            height = st.number_input(
                "Height (metres)",
                min_value=0.5,
                max_value=2.5,
                value=1.70,
                step=0.01,
                format="%.2f",
            )

        with col3:
            weight = st.number_input(
                "Weight (kg)",
                min_value=10.0,
                max_value=350.0,
                value=70.0,
                step=0.5,
            )

        gender = st.selectbox(
            "Gender",
            options=[
                "Female",
                "Male",
            ],
        )

        family_history = (
            st.selectbox(
                "Family history of overweight",
                options=[
                    "no",
                    "yes",
                ],
            )
        )

        st.divider()

        st.markdown(
            "### Eating Habits"
        )

        col1, col2 = (
            st.columns(2)
        )

        with col1:
            fcvc = st.number_input(
                "Vegetable consumption frequency (FCVC)",
                min_value=1.0,
                max_value=3.0,
                value=2.0,
                step=0.1,
                help=(
                    "Model input scale from "
                    "1.0 to 3.0."
                ),
            )

            ncp = st.number_input(
                "Number of main meals (NCP)",
                min_value=1.0,
                max_value=4.0,
                value=3.0,
                step=0.1,
            )

            caec = st.selectbox(
                "Food consumption between meals (CAEC)",
                options=[
                    "no",
                    "Sometimes",
                    "Frequently",
                    "Always",
                ],
            )

        with col2:
            favc = st.selectbox(
                "Frequent high-calorie food consumption (FAVC)",
                options=[
                    "no",
                    "yes",
                ],
            )

            ch2o = st.number_input(
                "Daily water consumption (CH2O)",
                min_value=1.0,
                max_value=3.0,
                value=2.0,
                step=0.1,
                help=(
                    "Model input scale from "
                    "1.0 to 3.0."
                ),
            )

            calc = st.selectbox(
                "Alcohol consumption (CALC)",
                options=[
                    "no",
                    "Sometimes",
                    "Frequently",
                ],
            )

        st.divider()

        st.markdown(
            "### Lifestyle and Activity"
        )

        col1, col2 = (
            st.columns(2)
        )

        with col1:
            faf = st.number_input(
                "Physical activity frequency (FAF)",
                min_value=0.0,
                max_value=3.0,
                value=1.0,
                step=0.1,
            )

            tue = st.number_input(
                "Technology use time (TUE)",
                min_value=0.0,
                max_value=2.0,
                value=1.0,
                step=0.1,
            )

            smoke = st.selectbox(
                "Do you smoke?",
                options=[
                    "no",
                    "yes",
                ],
            )

        with col2:
            scc = st.selectbox(
                "Do you monitor calorie consumption? (SCC)",
                options=[
                    "no",
                    "yes",
                ],
            )

            mtrans = st.selectbox(
                "Main transportation method",
                options=[
                    "Automobile",
                    "Bike",
                    "Motorbike",
                    "Public_Transportation",
                    "Walking",
                ],
            )

        st.divider()

        submitted = (
            st.form_submit_button(
                "Run Obesity Risk Assessment",
                type="primary",
                width="stretch",
            )
        )

    if not submitted:
        return None

    return {
        "Age": age,
        "Height": height,
        "Weight": weight,
        "FCVC": fcvc,
        "NCP": ncp,
        "CH2O": ch2o,
        "FAF": faf,
        "TUE": tue,
        "CAEC": caec,
        "CALC": calc,
        "Gender": gender,
        "family_history_with_overweight":
            family_history,
        "FAVC": favc,
        "SMOKE": smoke,
        "SCC": scc,
        "MTRANS": mtrans,
    }