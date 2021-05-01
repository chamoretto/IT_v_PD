from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import *

dev = APIRouter(
    prefix="/dev",
    tags=["developer"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)