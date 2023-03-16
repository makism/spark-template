import pytest

from template.utils import iso8601_to_minutes


@pytest.mark.parametrize(
    "pt_time, expected",
    [
        ("PT", 0),
        ("PT1H", 60),
        ("PT100M", 100),
        ("PT2H1M", 121),
    ],
)
def test_iso8601_to_minutes(pt_time: str, expected: int):
    assert iso8601_to_minutes(pt_time) == expected
