from datetime import datetime, timedelta, timezone


SRI_LANKA_TIMEZONE = timezone(
    timedelta(
        hours=5,
        minutes=30,
    )
)

SRI_LANKA_TIMEZONE_LABEL = "UTC+05:30"


def _parse_datetime(value):
    if value is None:
        return None

    text = str(value).strip()

    if not text:
        return None

    normalized = text

    if normalized.endswith("Z"):
        normalized = (
            normalized[:-1]
            + "+00:00"
        )

    try:
        parsed = datetime.fromisoformat(
            normalized
        )
    except ValueError:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=timezone.utc
        )

    return parsed.astimezone(
        SRI_LANKA_TIMEZONE
    )


def format_sri_lanka_datetime(value):
    if value is None:
        return "Unavailable"

    text = str(value).strip()

    if not text:
        return "Unavailable"

    if text.endswith(
        SRI_LANKA_TIMEZONE_LABEL
    ):
        return text

    local_time = _parse_datetime(
        value
    )

    if local_time is None:
        return text

    date_part = local_time.strftime(
        "%d %b %Y"
    )

    time_part = local_time.strftime(
        "%I:%M %p"
    ).lstrip("0")

    return (
        f"{date_part}, "
        f"{time_part} · "
        f"{SRI_LANKA_TIMEZONE_LABEL}"
    )


def format_sri_lanka_datetime_compact(
    value,
):
    if value is None:
        return "Unavailable"

    local_time = _parse_datetime(
        value
    )

    if local_time is None:
        text = str(value).strip()

        if " · UTC+05:30" in text:
            return text.replace(
                ",",
                "",
                1,
            ).replace(
                " · UTC+05:30",
                "",
            )

        return text or "Unavailable"

    date_part = local_time.strftime(
        "%d %b %Y"
    )

    time_part = local_time.strftime(
        "%I:%M %p"
    ).lstrip("0")

    return (
        f"{date_part} · "
        f"{time_part}"
    )


def localize_created_at(value):
    if isinstance(value, dict):
        localized = {}

        for key, item in value.items():
            if key == "created_at":
                localized[key] = (
                    format_sri_lanka_datetime(
                        item
                    )
                )
            else:
                localized[key] = (
                    localize_created_at(
                        item
                    )
                )

        return localized

    if isinstance(value, list):
        return [
            localize_created_at(item)
            for item in value
        ]

    return value