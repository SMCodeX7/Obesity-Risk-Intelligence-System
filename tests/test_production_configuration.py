from pathlib import Path

from backend import create_app
from backend.database import (
    get_configured_database_path,
)
from backend.production import (
    app as production_app,
    get_log_level,
)
from backend.run_production import (
    get_port,
)
from frontend.config import (
    DEFAULT_API_BASE_URL,
    get_api_base_url,
)


def test_default_api_base_url(
    monkeypatch,
):
    monkeypatch.delenv(
        "OBESITY_API_BASE_URL",
        raising=False,
    )

    assert (
        get_api_base_url()
        == DEFAULT_API_BASE_URL
    )


def test_environment_api_base_url(
    monkeypatch,
):
    monkeypatch.setenv(
        "OBESITY_API_BASE_URL",
        "https://example-api.com/",
    )

    assert (
        get_api_base_url()
        == "https://example-api.com"
    )


def test_database_environment_override(
    monkeypatch,
    tmp_path,
):
    database_path = (
        tmp_path
        / "production.db"
    )

    monkeypatch.setenv(
        "OBESITY_DATABASE_PATH",
        str(
            database_path
        ),
    )

    assert (
        get_configured_database_path()
        == database_path.resolve()
    )


def test_testing_database_override(
    tmp_path,
):
    database_path = (
        tmp_path
        / "testing.db"
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
        assert (
            get_configured_database_path()
            == database_path.resolve()
        )


def test_production_app_settings():
    assert (
        production_app.config[
            "DEBUG"
        ]
        is False
    )

    assert (
        production_app.config[
            "TESTING"
        ]
        is False
    )

    assert (
        production_app.config[
            "PROPAGATE_EXCEPTIONS"
        ]
        is False
    )


def test_production_port(
    monkeypatch,
):
    monkeypatch.setenv(
        "PORT",
        "8080",
    )

    assert get_port() == 8080

    monkeypatch.setenv(
        "PORT",
        "invalid",
    )

    assert get_port() == 5000


def test_production_log_level(
    monkeypatch,
):
    monkeypatch.setenv(
        "OBESITY_LOG_LEVEL",
        "WARNING",
    )

    assert (
        get_log_level()
        == "WARNING"
    )

    monkeypatch.setenv(
        "OBESITY_LOG_LEVEL",
        "INVALID",
    )

    assert (
        get_log_level()
        == "INFO"
    )