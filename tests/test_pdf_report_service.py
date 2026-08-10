from backend.services.pdf_report_service import (
    generate_prediction_report,
)


SAMPLE_PREDICTION = {
    "id": 10,

    "inputs": {
        "Age": 25.0,
        "Height": 1.70,
        "Weight": 70.0,
        "FCVC": 2.0,
        "NCP": 3.0,
        "CH2O": 2.0,
        "FAF": 1.0,
        "TUE": 1.0,
        "CAEC": "Sometimes",
        "CALC": "no",
        "Gender": "Male",
        "family_history_with_overweight":
            "yes",
        "FAVC": "yes",
        "SMOKE": "no",
        "SCC": "no",
        "MTRANS":
            "Public_Transportation",
    },

    "predicted_class":
        "Normal_Weight",

    "confidence":
        0.85,

    "probabilities": {
        "Insufficient_Weight":
            0.02,

        "Normal_Weight":
            0.85,

        "Overweight_Level_I":
            0.08,

        "Overweight_Level_II":
            0.03,

        "Obesity_Type_I":
            0.01,

        "Obesity_Type_II":
            0.005,

        "Obesity_Type_III":
            0.005,
    },

    "model_name":
        "Tuned Gradient Boosting",

    "scikit_learn_version":
        "1.8.0",

    "created_at":
        "2026-08-10 18:30:00",
}


def test_generate_prediction_report():
    pdf_bytes = (
        generate_prediction_report(
            SAMPLE_PREDICTION
        )
    )

    assert isinstance(
        pdf_bytes,
        bytes,
    )

    assert (
        pdf_bytes.startswith(
            b"%PDF"
        )
    )

    assert (
        len(
            pdf_bytes
        )
        > 1000
    )