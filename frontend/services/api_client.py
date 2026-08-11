import requests

from frontend.config import (
    get_api_base_url,
)


class APIClientError(
    Exception
):
    def __init__(
        self,
        message,
        status_code=None,
    ):
        super().__init__(
            message
        )

        self.status_code = (
            status_code
        )


class APIClient:
    def __init__(
        self,
        base_url=None,
        timeout=5,
    ):
        self.base_url = (
            base_url
            or get_api_base_url()
        ).rstrip(
            "/"
        )

        self.timeout = timeout

    def _request(
        self,
        method,
        endpoint,
        payload=None,
    ):
        url = (
            f"{self.base_url}"
            f"{endpoint}"
        )

        try:
            if method == "GET":
                response = (
                    requests.get(
                        url,
                        timeout=(
                            self.timeout
                        ),
                    )
                )

            elif method == "POST":
                response = (
                    requests.post(
                        url,
                        json=payload,
                        timeout=(
                            self.timeout
                        ),
                    )
                )

            else:
                raise APIClientError(
                    (
                        "Unsupported API "
                        "client request method."
                    )
                )

        except requests.RequestException as error:
            raise APIClientError(
                (
                    "Unable to communicate "
                    "with the backend API."
                )
            ) from error

        try:
            response_data = (
                response.json()
            )

        except ValueError as error:
            raise APIClientError(
                (
                    "Backend returned an "
                    "invalid JSON response."
                ),
                status_code=(
                    response.status_code
                ),
            ) from error

        if not response.ok:
            if isinstance(
                response_data,
                dict,
            ):
                message = (
                    response_data.get(
                        "message"
                    )
                    or response_data.get(
                        "error"
                    )
                )

            else:
                message = None

            if not message:
                message = (
                    "Backend request failed "
                    f"with HTTP "
                    f"{response.status_code}."
                )

            raise APIClientError(
                message,
                status_code=(
                    response.status_code
                ),
            )

        return response_data

    def get_health(
        self,
    ):
        return self._request(
            "GET",
            "/health",
        )

    def get_model_info(
        self,
    ):
        return self._request(
            "GET",
            "/model-info",
        )

    def predict(
        self,
        payload,
    ):
        return self._request(
            "POST",
            "/predict",
            payload=payload,
        )

    def get_predictions(
        self,
    ):
        return self._request(
            "GET",
            "/predictions",
        )

    def get_prediction(
        self,
        prediction_id,
    ):
        return self._request(
            "GET",
            (
                "/predictions/"
                f"{prediction_id}"
            ),
        )

    def get_prediction_report(
        self,
        prediction_id,
    ):
        url = (
            f"{self.base_url}"
            "/predictions/"
            f"{prediction_id}"
            "/report"
        )

        try:
            response = (
                requests.get(
                    url,
                    timeout=(
                        self.timeout
                    ),
                )
            )

        except requests.RequestException as error:
            raise APIClientError(
                (
                    "Unable to download "
                    "the PDF report."
                )
            ) from error

        if not response.ok:
            try:
                response_data = (
                    response.json()
                )

                if isinstance(
                    response_data,
                    dict,
                ):
                    message = (
                        response_data.get(
                            "message"
                        )
                        or response_data.get(
                            "error"
                        )
                    )

                else:
                    message = None

            except ValueError:
                message = None

            if not message:
                message = (
                    "PDF report request "
                    "failed with HTTP "
                    f"{response.status_code}."
                )

            raise APIClientError(
                message,
                status_code=(
                    response.status_code
                ),
            )

        return response.content