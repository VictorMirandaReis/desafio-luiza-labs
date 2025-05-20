from typing import Dict
from fastapi import UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.db.models import User, Order, OrderProduct
from datetime import datetime, date


class InvalidOrderError(Exception):
    pass


class OrderFileProcessor:
    def __init__(self, db: Session):
        self.db = db
        self.created_orders_count: int = 0
        self.error_count: int = 0

    def create_from_file(self, file: UploadFile) -> tuple[int, int]:
        content = file.file.read()
        lines = content.decode().splitlines()

        for line_num, line in enumerate(lines, start=1):
            if not line.strip():
                continue

            try:
                data = self._parse_line(line, line_num)
                user = self._get_or_create_user(data["user_id"], data["name"])
                order = self._get_or_create_order(
                    data["order_id"], user, data["purchase_date"])
                self._create_product_line(
                    order, data["product_id"], data["product_price"])
            except InvalidOrderError as e:
                self.error_count += 1
                print(e)

        self.db.commit()
        return self.created_orders_count, self.error_count

    def _parse_line(self, line: str, line_num: int) -> Dict:
        if line is None or len(line) < 95:
            raise Exception(f"Line {line_num} too short or None")

        try:
            raw_user_id = line[0:10].lstrip("0")
            raw_name = line[10:55].strip()
            raw_order_id = line[55:65].lstrip("0")
            raw_product_id = line[65:75].lstrip("0")
            raw_product_price = line[75:87].strip()
            raw_date = line[87:95].strip()

            if not raw_user_id.isdigit():
                raise ValueError(f"Invalid user_id: {raw_user_id}")
            user_id = int(raw_user_id)

            if not raw_order_id.isdigit():
                raise ValueError(f"Invalid order_id: {raw_order_id}")
            order_id = int(raw_order_id)

            if not raw_product_id.isdigit():
                raise ValueError(f"Invalid product_id: {raw_product_id}")
            product_id = int(raw_product_id)

            try:
                product_price = float(raw_product_price)
            except ValueError:
                raise ValueError(f"Invalid product_price: {raw_product_price}")

            if product_price < 0:
                raise ValueError(f"Negative product_price: {product_price}")

            try:
                purchase_date = datetime.strptime(raw_date, "%Y%m%d").date()
            except ValueError:
                raise ValueError(f"Invalid purchase_date: {raw_date}")

            if not raw_name:
                raise ValueError("Empty name")

            return {
                "user_id": user_id,
                "name": raw_name,
                "order_id": order_id,
                "product_id": product_id,
                "product_price": product_price,
                "purchase_date": purchase_date,
            }

        except Exception as e:
            raise InvalidOrderError(f"Failed to parse line {line_num}: {e}")

    def _get_or_create_user(self, external_id: int, name: str) -> User:
        res = self.db.execute(select(User).where(
            User.external_id == external_id))
        user = res.scalars().first()
        if user:
            return user

        user = User(external_id=external_id, name=name)
        self.db.add(user)
        self.db.flush()
        return user

    def _get_or_create_order(self, external_order_id: int, user: User, purchase_date: date) -> Order:
        res = self.db.execute(select(Order).where(
            Order.external_order_id == external_order_id))
        order = res.scalars().first()
        if order:
            return order

        order = Order(
            external_order_id=external_order_id,
            user_id=user.id,
            purchase_date=purchase_date
        )
        self.db.add(order)
        self.db.flush()
        self.created_orders_count += 1
        return order

    def _create_product_line(self, order: Order, external_product_id: int, price: float):
        res = self.db.execute(
            select(OrderProduct).where(
                OrderProduct.order_id == order.id,
                OrderProduct.external_product_id == external_product_id
            )
        )
        if res.scalars().first():
            return

        product = OrderProduct(
            order_id=order.id,
            external_product_id=external_product_id,
            price=price
        )
        self.db.add(product)
