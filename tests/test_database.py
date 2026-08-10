from backend import (
    create_app,
)
from backend.database import (
    get_db,
    init_db,
)


EXPECTED_COLUMNS = {
    "id",
    "age",
    "height",
    "weight",
    "fcvc",
    "ncp",
    "ch2o",
    "faf",
    "tue",
    "caec",
    "calc",
    "gender",
    "family_history_with_overweight",
    "favc",
    "smoke",
    "scc",
    "mtrans",
    "predicted_class",
    "confidence",
    "probabilities_json",
    "model_name",
    "scikit_learn_version",
    "created_at",
}


def test_database_initialization(
    tmp_path,
):
    database_path = (
        tmp_path
        / "test_obesity_risk.db"
    )

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(
                database_path
            ),
        }
    )

    with app.app_context():
        init_db()

        assert (
            database_path.exists()
        )

        database = get_db()

        table = database.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'prediction_history'
            """
        ).fetchone()

        assert table is not None

        assert (
            table["name"]
            == "prediction_history"
        )


def test_prediction_history_columns(
    tmp_path,
):
    database_path = (
        tmp_path
        / "test_columns.db"
    )

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(
                database_path
            ),
        }
    )

    with app.app_context():
        init_db()

        database = get_db()

        rows = database.execute(
            """
            PRAGMA table_info(
                prediction_history
            )
            """
        ).fetchall()

        column_names = {
            row["name"]
            for row in rows
        }

        assert (
            column_names
            == EXPECTED_COLUMNS
        )


def test_database_initialization_is_repeatable(
    tmp_path,
):
    database_path = (
        tmp_path
        / "test_repeat.db"
    )

    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(
                database_path
            ),
        }
    )

    with app.app_context():
        init_db()
        init_db()

        database = get_db()

        table = database.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            AND name = 'prediction_history'
            """
        ).fetchone()

        assert table is not None