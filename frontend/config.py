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


def get_boolean_setting(
    name,
    default=True,
):
    default_value = (
        "true"
        if default
        else "false"
    )

    value = os.getenv(
        name,
        default_value,
    )

    return (
        value.strip().lower()
        in {
            "1",
            "true",
            "yes",
            "on",
        }
    )


def is_history_ui_enabled():
    return get_boolean_setting(
        "OBESITY_SHOW_HISTORY",
        True,
    )