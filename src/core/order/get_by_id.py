from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import Optional
from src.db.models import Order


def get_order_by_id(
    id: int,
    db: Session
) -> Optional[Order]:
    stmt = (
        select(Order)
        .options(
            selectinload(Order.user),
            selectinload(Order.products),
        )
        .where(Order.external_order_id == id)
    )
    result = db.execute(stmt)
    return result.scalars().first()
