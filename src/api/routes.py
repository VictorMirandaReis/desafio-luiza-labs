from fastapi import APIRouter
from src.api.controllers.order_controller import (
    create_from_file,
    list_orders,
    find_by_id
)

router = APIRouter()
router.post("/orders", response_model=None)(create_from_file)
router.get("/orders", response_model=None)(list_orders)
router.get("/orders/{id}", response_model=None)(find_by_id)
