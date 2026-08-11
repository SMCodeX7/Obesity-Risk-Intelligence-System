from frontend.time_utils import (
    format_sri_lanka_datetime,
    localize_created_at,
)


def test_naive_utc_timestamp():
    result = format_sri_lanka_datetime(
        "2026-08-11 10:00:17"
    )

    assert (
        result
        == "11 Aug 2026, 3:30 PM · UTC+05:30"
    )


def test_utc_z_timestamp():
    result = format_sri_lanka_datetime(
        "2026-08-11T10:00:17Z"
    )

    assert (
        result
        == "11 Aug 2026, 3:30 PM · UTC+05:30"
    )


def test_utc_offset_timestamp():
    result = format_sri_lanka_datetime(
        "2026-08-11T10:00:17+00:00"
    )

    assert (
        result
        == "11 Aug 2026, 3:30 PM · UTC+05:30"
    )


def test_existing_sri_lanka_display():
    value = (
        "11 Aug 2026, "
        "3:30 PM · UTC+05:30"
    )

    assert (
        format_sri_lanka_datetime(
            value
        )
        == value
    )


def test_nested_created_at_conversion():
    payload = {
        "id": 16,
        "created_at":
            "2026-08-11 10:00:17",
        "result": {
            "created_at":
                "2026-08-11 10:00:17",
        },
    }

    localized = localize_created_at(
        payload
    )

    expected = (
        "11 Aug 2026, "
        "3:30 PM · UTC+05:30"
    )

    assert (
        localized["created_at"]
        == expected
    )

    assert (
        localized["result"][
            "created_at"
        ]
        == expected
    )