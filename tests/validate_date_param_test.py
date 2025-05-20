import pytest
from datetime import datetime
from fastapi import HTTPException

from src.api.utils.validators import validate_date_param

@pytest.mark.parametrize("invalid_date", [
    "19-05-2024",
    "2024/05/19",
    "2024-13-01",
    "2024-00-10",
    "2024-02-30",
    "",
    None
])
def test_validate_date_param_invalid_date(invalid_date):
    with pytest.raises(HTTPException) as exc_info:
        validate_date_param(invalid_date)
    assert exc_info.value.status_code == 400
    assert "Invalid Date" in exc_info.value.detail

def test_validate_date_param_valid_date():
    date_str = "2024-05-19"
    result = validate_date_param(date_str)
    assert isinstance(result, datetime)
    assert result.year == 2024
    assert result.month == 5
    assert result.day == 19
