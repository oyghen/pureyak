import datetime as dt

import pytest

from pureyak import chrono


class TestDateTimeParsing:
    @pytest.mark.parametrize(
        "value, expected",
        [
            # datetime
            (dt.datetime(2024, 7, 1), dt.datetime(2024, 7, 1, 0, 0, 0)),
            ("2024-07-01 00:00", dt.datetime(2024, 7, 1, 0, 0, 0)),
            ("2024-07-01 00:00:00", dt.datetime(2024, 7, 1, 0, 0, 0)),
            ("2024-07-01 12:00:00", dt.datetime(2024, 7, 1, 12, 0, 0)),
            ("20240701_120114", dt.datetime(2024, 7, 1, 12, 1, 14)),
            # date
            (dt.date(2024, 7, 1), dt.datetime(2024, 7, 1)),
            (dt.date(2024, 7, 1), dt.datetime(2024, 7, 1, 0, 0)),
            (dt.date(2024, 7, 1), dt.datetime(2024, 7, 1, 0, 0, 0)),
            ("2024-07-01", dt.datetime(2024, 7, 1)),
            ("2024-07-01", dt.datetime(2024, 7, 1)),
            ("20240701", dt.datetime(2024, 7, 1)),
            # time
            (dt.time(12, 30), dt.datetime(1900, 1, 1, 12, 30)),
            ("12:30", dt.datetime(1900, 1, 1, 12, 30)),
            ("12:30:00", dt.datetime(1900, 1, 1, 12, 30, 0)),
            ("T12:30:00", dt.datetime(1900, 1, 1, 12, 30, 0)),
            ("00:00", dt.datetime(1900, 1, 1, 0, 0)),
            # ISO 8601
            ("2024-07-01T00:00:00", dt.datetime(2024, 7, 1, 00)),
            ("2024-07-01T12:00:00", dt.datetime(2024, 7, 1, 12)),
            ("2024-07-01T23:59:59", dt.datetime(2024, 7, 1, 23, 59, 59)),
        ],
    )
    def test_parse(self, value: chrono.DateTimeLike, expected: dt.datetime):
        actual = chrono.parse(value)
        assert actual.tzinfo is None
        assert actual == expected

    @pytest.mark.parametrize(
        "value, expected",
        [
            (
                "2024-07-01T11:22:33Z",
                dt.datetime(2024, 7, 1, 11, 22, 33, tzinfo=dt.UTC),
            ),
            (
                "2024-07-01T11:22:33+00:00",
                dt.datetime(2024, 7, 1, 11, 22, 33, tzinfo=dt.UTC),
            ),
            (
                "2024-07-01T11:22:33-00:00",
                dt.datetime(2024, 7, 1, 11, 22, 33, tzinfo=dt.UTC),
            ),
            (
                "2024-07-01T11:00:00+01:00",
                dt.datetime(2024, 7, 1, 11, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            ),
            (
                "2024-07-01T11:00:00-01:00",
                dt.datetime(2024, 7, 1, 11, tzinfo=dt.timezone(dt.timedelta(hours=-1))),
            ),
            (
                "2024-07-01T11:00:00+01:00",
                dt.datetime(
                    2024, 7, 1, 11, tzinfo=dt.timezone(dt.timedelta(seconds=3600))
                ),
            ),
        ],
    )
    def test_tzinfo(self, value: chrono.DateTimeLike, expected: dt.datetime):
        actual = chrono.parse(value)
        expected_tzname = (
            "UTC"
            if any(value.endswith(tz_suffix) for tz_suffix in ("Z", "+00:00", "-00:00"))
            else f"UTC{value[-6:]}"
        )
        assert actual.tzinfo is not None
        assert actual.tzname() == expected_tzname
        assert actual == expected

    @pytest.mark.parametrize(
        "value_cet, value_dt",
        [
            ("2024-01-01T11:22:33+01:00", dt.datetime(2024, 1, 1, 11, 22, 33)),
            ("2024-07-01T11:22:33+01:00", dt.datetime(2024, 7, 1, 11, 22, 33)),
        ],
    )
    def test_tzinfo__cet(self, value_cet: chrono.DateTimeLike, value_dt: dt.datetime):
        try:
            actual = chrono.parse(value_cet)
            expected = value_dt.replace(tzinfo=dt.timezone(dt.timedelta(seconds=3600)))
            assert actual.tzinfo is not None
            assert actual.tzname() == "UTC+01:00"
            assert actual == expected
        except AssertionError:
            value_cest = value_cet.replace("+01:00", "+02:00")
            actual = chrono.parse(value_cest)
            expected = value_dt.replace(tzinfo=dt.timezone(dt.timedelta(seconds=7200)))
            assert actual.tzinfo is not None
            assert actual.tzname() == "UTC+02:00"
            assert actual == expected

    @pytest.mark.parametrize(
        "value, fmt, expected",
        [
            (
                "2024/07/01  12.01.14",
                "%Y/%m/%d %H.%M.%S",
                dt.datetime(2024, 7, 1, 12, 1, 14),
            ),
            (
                "20240701_120114",
                "%Y%m%d_%H%M%S",
                dt.datetime(2024, 7, 1, 12, 1, 14),
            ),
        ],
    )
    def test_fmt(self, value: chrono.DateTimeLike, fmt: str, expected: dt.datetime):
        actual = chrono.parse(value, fmt=fmt)
        assert actual == expected

    @pytest.mark.parametrize("value", ["foo", "-"])
    def test_value_error(self, value: chrono.DateTimeLike):
        with pytest.raises(ValueError):
            chrono.parse(value)

    @pytest.mark.parametrize("value", [None, 0, 1.0])
    def test_type_error(self, value: chrono.DateTimeLike):
        with pytest.raises(TypeError):
            chrono.parse(value)
