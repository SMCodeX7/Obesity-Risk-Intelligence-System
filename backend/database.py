import sqlite3
from pathlib import Path

import click
from flask import (
    current_app,
    g,
)
from flask.cli import (
    with_appcontext,
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


def get_db():
    if "database" not in g:

        database_path = Path(
            current_app.config[
                "DATABASE"
            ]
        )

        database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        connection = (
            sqlite3.connect(
                str(
                    database_path
                )
            )
        )

        connection.row_factory = (
            sqlite3.Row
        )

        connection.execute(
            "PRAGMA foreign_keys = ON"
        )

        g.database = connection

    return g.database


def close_db(
    error=None,
):
    connection = g.pop(
        "database",
        None,
    )

    if connection is not None:
        connection.close()


def init_db():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            "Database schema file "
            f"not found: {SCHEMA_PATH}"
        )

    connection = get_db()

    schema_sql = (
        SCHEMA_PATH.read_text(
            encoding="utf-8"
        )
    )

    connection.executescript(
        schema_sql
    )

    connection.commit()


@click.command(
    "init-db"
)
@with_appcontext
def init_db_command():
    init_db()

    click.echo(
        "Database initialized: "
        f"{current_app.config['DATABASE']}"
    )


def init_app(
    app,
):
    app.teardown_appcontext(
        close_db
    )

    app.cli.add_command(
        init_db_command
    )