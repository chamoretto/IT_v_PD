from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import *

smm = APIRouter(
    prefix="/smm",
    tags=["smm"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)