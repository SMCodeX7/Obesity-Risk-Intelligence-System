from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    OrdinalEncoder,
    StandardScaler,
)


NUMERICAL_FEATURES = [
    "Age",
    "Height",
    "Weight",
    "FCVC",
    "NCP",
    "CH2O",
    "FAF",
    "TUE",
]

ORDINAL_FEATURES = [
    "CAEC",
    "CALC",
]

NOMINAL_FEATURES = [
    "Gender",
    "family_history_with_overweight",
    "FAVC",
    "SMOKE",
    "SCC",
    "MTRANS",
]

ORDINAL_CATEGORY_ORDERS = {
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
    ],
}

PREDICTIVE_FEATURES = (
    NUMERICAL_FEATURES
    + ORDINAL_FEATURES
    + NOMINAL_FEATURES
)

if len(PREDICTIVE_FEATURES) != len(
    set(PREDICTIVE_FEATURES)
):
    raise ValueError(
        "A predictive feature appears in more than one group."
    )


def build_preprocessor() -> ColumnTransformer:
    ordinal_categories = [
        ORDINAL_CATEGORY_ORDERS[column]
        for column in ORDINAL_FEATURES
    ]

    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    ordinal_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OrdinalEncoder(
                    categories=ordinal_categories,
                    handle_unknown="use_encoded_value",
                    unknown_value=-1,
                ),
            ),
        ]
    )

    nominal_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent"),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            (
                "numerical",
                numerical_pipeline,
                NUMERICAL_FEATURES,
            ),
            (
                "ordinal",
                ordinal_pipeline,
                ORDINAL_FEATURES,
            ),
            (
                "nominal",
                nominal_pipeline,
                NOMINAL_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )