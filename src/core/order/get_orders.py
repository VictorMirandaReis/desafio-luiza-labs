from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, Sequence
from src.db.models import Order


def get_orders(
    db: Session,
    user_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    page: int = 1,
    page_size: int = 25,
) -> Sequence[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.user),
            selectinload(Order.products),
        )
        .order_by(Order.user_id)
    )

    if user_id:
        stmt = stmt.where(Order.user_id == user_id)

    if start_date:
        stmt = stmt.where(Order.purchase_date >= start_date.date())

    if end_date:
        stmt = stmt.where(Order.purchase_date <= end_date.date())

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size)

    result = db.execute(stmt)
    orders = result.scalars().all()

    return orders
