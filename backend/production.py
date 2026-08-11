import logging
import os

from backend import create_app


VALID_LOG_LEVELS = {
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
}


def get_log_level():
    configured_level = (
        os.getenv(
            "OBESITY_LOG_LEVEL",
            "INFO",
        )
        .strip()
        .upper()
    )

    if (
        configured_level
        not in VALID_LOG_LEVELS
    ):
        return "INFO"

    return configured_level


def configure_logging():
    logging.basicConfig(
        level=getattr(
            logging,
            get_log_level(),
        ),
        format=(
            "%(asctime)s "
            "%(levelname)s "
            "%(name)s "
            "%(message)s"
        ),
    )


def create_production_app():
    configure_logging()

    app = create_app()

    app.config.update(
        DEBUG=False,
        TESTING=False,
        PROPAGATE_EXCEPTIONS=False,
    )

    return app


app = create_production_app()