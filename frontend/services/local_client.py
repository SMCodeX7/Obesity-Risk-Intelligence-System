import streamlit as st

from backend import create_app
from frontend.services.api_client import APIClient, APIClientError


@st.cache_resource
def get_backend_app():
    return create_app()


class LocalAPIClient(APIClient):
    def __init__(self):
        self.app = get_backend_app()

    def _request(self, method, endpoint, payload=None):
        with self.app.test_client() as client:
            response = client.open(
                endpoint,
                method=method,
                json=payload,
            )

        data = response.get_json()

        if response.status_code >= 400:
            error = data or {}
            raise APIClientError(
                error.get("message")
                or error.get("error")
                or "Request failed.",
                status_code=response.status_code,
            )

        return data

    def get_prediction_report(self, prediction_id):
        with self.app.test_client() as client:
            response = client.get(
                f"/predictions/{prediction_id}/report"
            )

        if response.status_code >= 400:
            error = response.get_json() or {}
            raise APIClientError(
                error.get("message")
                or error.get("error")
                or "PDF download failed.",
                status_code=response.status_code,
            )

        return response.data