from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from typing import Optional

def success_response(message: str, data: Optional[dict] = None):
    body = {"message": message}
    if data:
        body.update(data)
    return JSONResponse(content=body, status_code=200)

def InvalidRequestError(detail: str = "Invalid request"):
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

def NotFoundError(detail: str = "Resource not found"):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

