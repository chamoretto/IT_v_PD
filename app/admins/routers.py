from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import *

admin = APIRouter(
    prefix="/admin",
    tags=["admin"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)