import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer

from src.preprocessing import (
    NOMINAL_FEATURES,
    NUMERICAL_FEATURES,
    ORDINAL_FEATURES,
    PREDICTIVE_FEATURES,
    build_preprocessor,
)


def create_sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Age": [18.0, 25.0, 35.0, 45.0],
            "Height": [1.60, 1.70, 1.75, 1.80],
            "Weight": [50.0, 70.0, 90.0, 110.0],
            "FCVC": [2.0, 3.0, 2.5, 1.0],
            "NCP": [3.0, 3.0, 4.0, 2.0],
            "CH2O": [2.0, 2.5, 3.0, 1.5],
            "FAF": [1.0, 2.0, 0.5, 0.0],
            "TUE": [1.0, 0.5, 2.0, 1.5],
            "CAEC": [
                "no",
                "Sometimes",
                "Frequently",
                "Always",
            ],
            "CALC": [
                "no",
                "Sometimes",
                "Frequently",
                "no",
            ],
            "Gender": [
                "Female",
                "Male",
                "Female",
                "Male",
            ],
            "family_history_with_overweight": [
                "no",
                "yes",
                "yes",
                "no",
            ],
            "FAVC": [
                "no",
                "yes",
                "yes",
                "no",
            ],
            "SMOKE": [
                "no",
                "no",
                "yes",
                "no",
            ],
            "SCC": [
                "yes",
                "no",
                "no",
                "yes",
            ],
            "MTRANS": [
                "Walking",
                "Public_Transportation",
                "Automobile",
                "Bike",
            ],
        }
    )


def test_feature_group_configuration():
    assert len(NUMERICAL_FEATURES) == 8
    assert len(ORDINAL_FEATURES) == 2
    assert len(NOMINAL_FEATURES) == 6
    assert len(PREDICTIVE_FEATURES) == 16

    assert len(PREDICTIVE_FEATURES) == len(
        set(PREDICTIVE_FEATURES)
    )

    assert PREDICTIVE_FEATURES == (
        NUMERICAL_FEATURES
        + ORDINAL_FEATURES
        + NOMINAL_FEATURES
    )


def test_build_preprocessor_returns_new_objects():
    first_preprocessor = build_preprocessor()
    second_preprocessor = build_preprocessor()

    assert isinstance(
        first_preprocessor,
        ColumnTransformer,
    )

    assert isinstance(
        second_preprocessor,
        ColumnTransformer,
    )

    assert first_preprocessor is not second_preprocessor


def test_preprocessor_transforms_training_data():
    sample_data = create_sample_data()
    preprocessor = build_preprocessor()

    transformed_data = preprocessor.fit_transform(
        sample_data
    )

    feature_names = (
        preprocessor.get_feature_names_out()
    )

    assert transformed_data.shape[0] == len(
        sample_data
    )

    assert transformed_data.shape[1] == len(
        feature_names
    )

    assert np.isfinite(transformed_data).all()


def test_preprocessor_handles_missing_values():
    sample_data = create_sample_data()

    sample_data.loc[0, "Age"] = np.nan
    sample_data.loc[1, "CAEC"] = np.nan
    sample_data.loc[2, "Gender"] = np.nan

    preprocessor = build_preprocessor()

    transformed_data = preprocessor.fit_transform(
        sample_data
    )

    assert np.isfinite(transformed_data).all()


def test_preprocessor_handles_unknown_categories():
    training_data = create_sample_data()
    preprocessor = build_preprocessor()

    preprocessor.fit(training_data)

    new_data = training_data.iloc[[0]].copy()

    new_data.loc[:, "CAEC"] = "Rarely"
    new_data.loc[:, "MTRANS"] = "Scooter"

    transformed_data = preprocessor.transform(
        new_data
    )

    feature_names = list(
        preprocessor.get_feature_names_out()
    )

    caec_column_index = feature_names.index(
        "ordinal__CAEC"
    )

    assert transformed_data.shape[0] == 1
    assert np.isfinite(transformed_data).all()

    assert (
        transformed_data[0, caec_column_index]
        == -1
    )