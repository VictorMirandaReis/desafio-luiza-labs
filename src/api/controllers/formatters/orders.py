from typing import Optional, Sequence, List, Dict, Any
from src.db.models import Order


def format_list_orders_response(orders: Sequence[Order]) -> List[Dict[str, Any]]:
    response = []

    for order in orders:
        user_id = order.user.external_id
        user_name = order.user.name

        user = next((u for u in response if u["user_id"] == user_id), None)
        if not user:
            user = {"user_id": user_id, "name": user_name, "orders": []}
            response.append(user)

        products = [
            {"product_id": p.external_product_id, "value": f"{p.price:.2f}"}
            for p in order.products
        ]

        total_value = sum(p.price for p in order.products)

        user["orders"].append({
            "order_id": order.external_order_id,
            "total": f"{total_value:.2f}",
            "date": order.purchase_date.strftime("%Y-%m-%d"),
            "products": products,
        })

    return response


def format_find_by_id_response(order: Optional[Order]) -> Optional[Dict[str, Any]]:
    if not order:
        return None

    products = [
        {
            "product_id": p.external_product_id,
            "value": f"{p.price:.2f}"
        }
        for p in order.products
    ]

    total_value = sum(p.price for p in order.products)

    return {
        "user_id": order.user.external_id,
        "name": order.user.name,
        "orders": [
            {
                "order_id": order.external_order_id,
                "total": f"{total_value:.2f}",
                "date": order.purchase_date.strftime("%Y-%m-%d"),
                "products": products,
            }
        ]
    }
