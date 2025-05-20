from datetime import date
from src.api.controllers.formatters.orders import format_find_by_id_response, format_list_orders_response
from src.db.models import User, Order, OrderProduct


def make_user(id=1, external_id=1001, name="Alice"):
    user = User(id=id, external_id=external_id, name=name)
    return user


def make_product(id, external_product_id, price):
    product = OrderProduct(id=id, external_product_id=external_product_id, price=price)
    return product


def make_order(id, external_order_id, user, products, purchase_date=date(2024, 5, 10)):
    order = Order(
        id=id,
        external_order_id=external_order_id,
        user=user,
        purchase_date=purchase_date
    )
    order.products = products
    return order


def test_format_list_orders_response_single_order():
    user = make_user()
    products = [
        make_product(1, 2001, 10.0),
        make_product(2, 2002, 20.5),
    ]
    order = make_order(1, 3001, user, products)

    user.orders = [order]
    order.user = user
    for p in products:
        p.order = order

    result = format_list_orders_response([order])

    assert len(result) == 1
    assert result[0]["user_id"] == 1001
    assert result[0]["name"] == "Alice"
    assert len(result[0]["orders"]) == 1

    order_data = result[0]["orders"][0]
    assert order_data["order_id"] == 3001
    assert order_data["total"] == "30.50"
    assert order_data["date"] == "2024-05-10"
    assert order_data["products"] == [
        {"product_id": 2001, "value": "10.00"},
        {"product_id": 2002, "value": "20.50"},
    ]


def test_format_list_orders_response_multiple_users():
    user1 = make_user(1, 1001, "Alice")
    user2 = make_user(2, 1002, "Bob")

    order1 = make_order(1, 3001, user1, [make_product(1, 2001, 15.0)])
    order2 = make_order(2, 3002, user2, [make_product(2, 2002, 25.0)])

    order1.user = user1
    order2.user = user2

    result = format_list_orders_response([order1, order2])

    assert len(result) == 2
    assert {u["user_id"] for u in result} == {1001, 1002}


def test_format_list_orders_response_multiple_orders_same_user():
    user = make_user()
    order1 = make_order(1, 3001, user, [make_product(1, 2001, 10.0)])
    order2 = make_order(2, 3002, user, [make_product(2, 2002, 20.0)])

    result = format_list_orders_response([order1, order2])

    assert len(result) == 1
    assert result[0]["user_id"] == 1001
    assert len(result[0]["orders"]) == 2


def test_format_find_by_id_response_valid():
    user = make_user()
    products = [
        make_product(1, 2001, 5.25),
        make_product(2, 2002, 14.75),
    ]
    order = make_order(1, 3001, user, products)

    order.user = user
    user.orders = [order]
    for p in products:
        p.order = order
    order.products = products

    result = format_find_by_id_response(order)

    assert result is not None
    assert result["user_id"] == 1001
    assert result["name"] == "Alice"
    assert len(result["orders"]) == 1

    order_data = result["orders"][0]
    assert order_data["order_id"] == 3001
    assert order_data["total"] == "20.00"
    assert order_data["date"] == "2024-05-10"
    assert order_data["products"] == [
        {"product_id": 2001, "value": "5.25"},
        {"product_id": 2002, "value": "14.75"},
    ]


def test_format_find_by_id_response_none():
    assert format_find_by_id_response(None) is None
