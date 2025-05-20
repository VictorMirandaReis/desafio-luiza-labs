from fastapi import UploadFile
from src.api.utils.responses import InvalidRequestError
from datetime import datetime


def validate_date_param(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        raise InvalidRequestError(f"Invalid Date: {date_str}. Expected format: YYYY-MM-DD")
