from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel


dev = APIRouter(
    prefix="/dev",
    tags=["developer"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@dev.get('/')
async def start_dev():
    return {1: 1}