from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import *

user = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)