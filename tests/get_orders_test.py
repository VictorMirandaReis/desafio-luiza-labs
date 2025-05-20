import pytest
from unittest.mock import MagicMock
from datetime import datetime, date
from src.core.order.get_orders import get_orders
from src.db.models import Order


@pytest.fixture
def mock_order():
    order = MagicMock(spec=Order)
    order.user_id = 1001
    order.purchase_date = date(2024, 5, 1)
    order.user = MagicMock()
    order.user.name = "Victor"
    order.products = []
    return order


def test_get_orders_no_filters(mock_order):
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_order]
    mock_db.execute.return_value = mock_result

    result = get_orders(mock_db)

    assert len(result) == 1
    assert result[0].user_id == 1001  # type: ignore


def test_get_orders_with_user_id(mock_order):
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_order]
    mock_db.execute.return_value = mock_result

    result = get_orders(mock_db, user_id=1001) # type: ignore

    assert len(result) == 1
    assert result[0].user_id == 1001  # type: ignore


def test_get_orders_with_start_date(mock_order):
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_order]
    mock_db.execute.return_value = mock_result

    start_date = datetime(2024, 4, 1)
    result = get_orders(mock_db, start_date=start_date)

    assert len(result) == 1
    assert result[0].purchase_date >= start_date.date()  # type: ignore


def test_get_orders_with_end_date(mock_order):
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_order]
    mock_db.execute.return_value = mock_result

    end_date = datetime(2024, 6, 1)
    result = get_orders(mock_db, end_date=end_date)

    assert len(result) == 1
    assert result[0].purchase_date <= end_date.date()  # type: ignore


def test_get_orders_with_pagination(mock_order):
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_order]
    mock_db.execute.return_value = mock_result

    result = get_orders(mock_db, page=2, page_size=10)

    assert len(result) == 1
    assert result[0].user_id == 1001  # type: ignore
