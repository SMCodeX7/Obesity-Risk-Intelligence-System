import os
import sqlite3
from pathlib import Path

from flask import (
    current_app,
    g,
    has_app_context,
)


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

DEFAULT_DATABASE_PATH = (
    PROJECT_ROOT
    / "database"
    / "obesity_risk.db"
)

SCHEMA_PATH = (
    PROJECT_ROOT
    / "database"
    / "schema.sql"
)


def _resolve_path(
    value,
):
    database_path = Path(
        value
    ).expanduser()

    if not database_path.is_absolute():
        database_path = (
            PROJECT_ROOT
            / database_path
        )

    return database_path.resolve()


def get_configured_database_path():
    if has_app_context():
        app_database = (
            current_app.config.get(
                "DATABASE"
            )
        )

        if (
            current_app.config.get(
                "TESTING",
                False,
            )
            and app_database
        ):
            return _resolve_path(
                app_database
            )

    environment_database = (
        os.getenv(
            "OBESITY_DATABASE_PATH"
        )
    )

    if environment_database:
        return _resolve_path(
            environment_database
        )

    if has_app_context():
        app_database = (
            current_app.config.get(
                "DATABASE"
            )
        )

        if app_database:
            return _resolve_path(
                app_database
            )

    return DEFAULT_DATABASE_PATH


DATABASE_PATH = (
    _resolve_path(
        os.getenv(
            "OBESITY_DATABASE_PATH",
            str(
                DEFAULT_DATABASE_PATH
            ),
        )
    )
)


def ensure_database_directory(
    database_path=None,
):
    path = (
        database_path
        or get_configured_database_path()
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


def create_connection(
    database_path=None,
):
    path = (
        database_path
        or get_configured_database_path()
    )

    ensure_database_directory(
        path
    )

    connection = sqlite3.connect(
        str(
            path
        ),
        timeout=30,
    )

    connection.row_factory = (
        sqlite3.Row
    )

    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    connection.execute(
        "PRAGMA busy_timeout = 30000"
    )

    return connection


def get_db():
    if "db" not in g:
        g.db = (
            create_connection()
        )

    return g.db


def get_connection():
    return create_connection()


def get_database_connection():
    return create_connection()


def close_db(
    error=None,
):
    database = g.pop(
        "db",
        None,
    )

    if database is not None:
        database.close()


def _read_schema():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            (
                "Database schema file "
                "was not found: "
                f"{SCHEMA_PATH}"
            )
        )

    return SCHEMA_PATH.read_text(
        encoding="utf-8"
    )


def init_db():
    database = get_db()

    database.executescript(
        _read_schema()
    )

    database.commit()


def initialize_database():
    database_path = (
        get_configured_database_path()
    )

    connection = (
        create_connection(
            database_path
        )
    )

    try:
        connection.executescript(
            _read_schema()
        )

        connection.commit()

    finally:
        connection.close()


def init_app(
    app,
):
    app.teardown_appcontext(
        close_db
    )

    with app.app_context():
        init_db()


def database_exists():
    database_path = (
        get_configured_database_path()
    )

    return database_path.exists()