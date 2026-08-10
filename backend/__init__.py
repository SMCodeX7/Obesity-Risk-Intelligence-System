from flask import Flask

from backend.routes.health import health_bp


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is not None:
        app.config.update(
            test_config
        )

    app.register_blueprint(
        health_bp
    )

    return app