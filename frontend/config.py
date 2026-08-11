import os


DEFAULT_API_BASE_URL = (
    "http://127.0.0.1:5000"
)


def get_api_base_url():
    configured_url = (
        os.getenv(
            "OBESITY_API_BASE_URL",
            DEFAULT_API_BASE_URL,
        )
        .strip()
    )

    if not configured_url:
        configured_url = (
            DEFAULT_API_BASE_URL
        )

    return configured_url.rstrip(
        "/"
    )