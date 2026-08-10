import os

import requests


DEFAULT_API_BASE_URL = (
    "http://127.0.0.1:5000"
)


class APIClientError(Exception):
    pass


class APIClient:
    def __init__(
        self,
        base_url=None,
        timeout=5,
    ):
        self.base_url = (
            base_url
            or os.getenv(
                "OBESITY_API_BASE_URL",
                DEFAULT_API_BASE_URL,
            )
        ).rstrip("/")

        self.timeout = timeout

    def _get(
        self,
        endpoint,
    ):
        url = (
            f"{self.base_url}"
            f"{endpoint}"
        )

        try:
            response = requests.get(
                url,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:
            raise APIClientError(
                "Unable to communicate "
                "with the backend API: "
                f"{error}"
            ) from error

        except ValueError as error:
            raise APIClientError(
                "Backend returned an "
                "invalid JSON response"
            ) from error

    def _post(
        self,
        endpoint,
        payload,
    ):
        url = (
            f"{self.base_url}"
            f"{endpoint}"
        )

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:
            raise APIClientError(
                "Unable to complete "
                "the API request: "
                f"{error}"
            ) from error

        except ValueError as error:
            raise APIClientError(
                "Backend returned an "
                "invalid JSON response"
            ) from error

    def get_health(self):
        return self._get(
            "/health"
        )

    def get_model_info(self):
        return self._get(
            "/model-info"
        )

    def predict(
        self,
        payload,
    ):
        return self._post(
            "/predict",
            payload,
        )