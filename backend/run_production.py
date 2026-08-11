import os

from waitress import serve

from backend.production import app


def get_port():
    configured_port = os.getenv(
        "PORT",
        "5000",
    )

    try:
        port = int(
            configured_port
        )
    except ValueError:
        return 5000

    if not (
        1 <= port <= 65535
    ):
        return 5000

    return port


def run():
    serve(
        app,
        host="0.0.0.0",
        port=get_port(),
        threads=4,
    )


if __name__ == "__main__":
    run()