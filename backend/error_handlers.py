from backend.exceptions import (
    ValidationError,
)


def register_error_handlers(
    app,
):
    @app.errorhandler(
        ValidationError
    )
    def handle_validation_error(
        error,
    ):
        return {
            "error":
                "validation_error",

            "message":
                str(error),
        }, 400

    @app.errorhandler(404)
    def handle_not_found(
        error,
    ):
        return {
            "error":
                "not_found",

            "message":
                "The requested endpoint "
                "does not exist.",
        }, 404

    @app.errorhandler(405)
    def handle_method_not_allowed(
        error,
    ):
        return {
            "error":
                "method_not_allowed",

            "message":
                "The HTTP method is not "
                "allowed for this endpoint.",
        }, 405

    @app.errorhandler(500)
    def handle_internal_server_error(
        error,
    ):
        return {
            "error":
                "internal_server_error",

            "message":
                "An unexpected server "
                "error occurred.",
        }, 500