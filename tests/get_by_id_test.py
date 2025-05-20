import pytest
from unittest.mock import MagicMock
from datetime import datetime
from src.core.order.get_by_id import get_order_by_id
from src.db.models import Order, User, OrderProduct


@pytest.fixture
def mock_order():
    order = MagicMock(spec=Order)
    order.external_order_id = 123
    order.purchase_date = datetime(2024, 5, 1)

    user = MagicMock(spec=User)
    user.name = "Victor"
    order.user = user

    product1 = MagicMock(spec=OrderProduct)
    product1.external_product_id = 456
    product1.price = 100.0

    product2 = MagicMock(spec=OrderProduct)
    product2.external_product_id = 789
    product2.price = 150.0

    order.products = [product1, product2]

    return order


def test_get_order_by_id_found(mock_order):
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_order
    mock_db.execute.return_value = mock_result

    result = get_order_by_id(123, db=mock_db)

    assert result is not None
    assert result.external_order_id == 123
    assert result.user.name == "Victor"
    assert len(result.products) == 2
    assert result.products[0].price == 100.0


def test_get_order_by_id_not_found():
    mock_db = MagicMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    result = get_order_by_id(999, db=mock_db)

    assert result is None
