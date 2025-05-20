from fastapi import Depends, Path, Query, UploadFile
from typing import Optional
from src.api.controllers.formatters.orders import format_find_by_id_response, format_list_orders_response
from src.api.utils.responses import InvalidRequestError, NotFoundError, success_response
from src.api.utils.validators import validate_date_param
from src.core.order.create_from_file import OrderFileProcessor
from src.core.order.get_orders import get_orders
from src.core.order.get_by_id import get_order_by_id
from src.db.database import get_db
from sqlalchemy.orm import Session


def create_from_file(
    file: UploadFile,
    db: Session = Depends(get_db)
):
    if not file.filename or not file.filename.lower().endswith(".txt"):
        raise InvalidRequestError("Only .txt files are allowed.")

    order_processor = OrderFileProcessor(db)
    num_created, num_failed = order_processor.create_from_file(file)

    return success_response(
        "Orders created successfully.",
        {
            "total_created": num_created,
            "total_failed": num_failed,
        })


def list_orders(
    user_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    valid_start_date = validate_date_param(start_date) if start_date else None
    valid_end_date = validate_date_param(end_date) if end_date else None

    if valid_start_date and valid_end_date and valid_start_date > valid_end_date:
        raise InvalidRequestError(
            "start_date cannot be greater than end_date.")

    if user_id and not user_id.isdigit():
        raise InvalidRequestError("user id should be numeric.")

    orders = get_orders(
        db=db,
        user_id=user_id,
        start_date=valid_start_date,
        end_date=valid_end_date,
        page=page,
        page_size=page_size
    )

    return format_list_orders_response(orders)


def find_by_id(
    id: str = Path(...),
    db: Session = Depends(get_db)
):
    if not id.isdigit():
        raise InvalidRequestError("Order Id must be numeric.")

    order = format_find_by_id_response(get_order_by_id(int(id), db))

    if not order:
        raise NotFoundError("Order not found.")

    return order
