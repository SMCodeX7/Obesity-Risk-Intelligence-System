from flask import Flask

from backend.routes.health import (
    health_bp,
)
from backend.routes.model_info import (
    model_info_bp,
)
from backend.routes.prediction import (
    prediction_bp,
)
from backend.services.model_service import (
    ModelService,
)


def create_app(
    test_config=None,
):
    app = Flask(
        __name__
    )

    if test_config is not None:
        app.config.update(
            test_config
        )

    model_service = (
        ModelService()
    )

    app.extensions[
        "obesity_risk_model"
    ] = model_service

    app.register_blueprint(
        health_bp
    )

    app.register_blueprint(
        model_info_bp
    )

    app.register_blueprint(
        prediction_bp
    )

    return app