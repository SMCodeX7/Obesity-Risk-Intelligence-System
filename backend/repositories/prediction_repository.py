import json

from backend.database import get_db


def save_prediction(
    features,
    prediction_result,
    model_metadata,
):
    database = get_db()

    probabilities_json = json.dumps(
        prediction_result[
            "probabilities"
        ]
    )

    cursor = database.execute(
        """
        INSERT INTO prediction_history (
            age,
            height,
            weight,
            fcvc,
            ncp,
            ch2o,
            faf,
            tue,
            caec,
            calc,
            gender,
            family_history_with_overweight,
            favc,
            smoke,
            scc,
            mtrans,
            predicted_class,
            confidence,
            probabilities_json,
            model_name,
            scikit_learn_version
        )
        VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?
        )
        """,
        (
            features["Age"],
            features["Height"],
            features["Weight"],
            features["FCVC"],
            features["NCP"],
            features["CH2O"],
            features["FAF"],
            features["TUE"],
            features["CAEC"],
            features["CALC"],
            features["Gender"],
            features[
                "family_history_with_overweight"
            ],
            features["FAVC"],
            features["SMOKE"],
            features["SCC"],
            features["MTRANS"],
            prediction_result[
                "predicted_class"
            ],
            prediction_result[
                "confidence"
            ],
            probabilities_json,
            model_metadata[
                "selected_candidate"
            ],
            model_metadata[
                "scikit_learn_version"
            ],
        ),
    )

    database.commit()

    return cursor.lastrowid


def list_predictions(
    limit=50,
):
    database = get_db()

    rows = database.execute(
        """
        SELECT
            id,
            predicted_class,
            confidence,
            model_name,
            scikit_learn_version,
            created_at
        FROM prediction_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            limit,
        ),
    ).fetchall()

    return [
        {
            "id":
                row["id"],

            "predicted_class":
                row["predicted_class"],

            "confidence":
                row["confidence"],

            "model_name":
                row["model_name"],

            "scikit_learn_version":
                row[
                    "scikit_learn_version"
                ],

            "created_at":
                row["created_at"],
        }
        for row in rows
    ]


def get_prediction(
    prediction_id,
):
    database = get_db()

    row = database.execute(
        """
        SELECT *
        FROM prediction_history
        WHERE id = ?
        """,
        (
            prediction_id,
        ),
    ).fetchone()

    if row is None:
        return None

    probabilities = json.loads(
        row[
            "probabilities_json"
        ]
    )

    return {
        "id":
            row["id"],

        "inputs": {
            "Age":
                row["age"],

            "Height":
                row["height"],

            "Weight":
                row["weight"],

            "FCVC":
                row["fcvc"],

            "NCP":
                row["ncp"],

            "CH2O":
                row["ch2o"],

            "FAF":
                row["faf"],

            "TUE":
                row["tue"],

            "CAEC":
                row["caec"],

            "CALC":
                row["calc"],

            "Gender":
                row["gender"],

            "family_history_with_overweight":
                row[
                    "family_history_with_overweight"
                ],

            "FAVC":
                row["favc"],

            "SMOKE":
                row["smoke"],

            "SCC":
                row["scc"],

            "MTRANS":
                row["mtrans"],
        },

        "predicted_class":
            row["predicted_class"],

        "confidence":
            row["confidence"],

        "probabilities":
            probabilities,

        "model_name":
            row["model_name"],

        "scikit_learn_version":
            row[
                "scikit_learn_version"
            ],

        "created_at":
            row["created_at"],
    }