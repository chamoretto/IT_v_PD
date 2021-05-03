from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel


smm = APIRouter(
    prefix="/smm",
    tags=["smm"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@smm.get('/')
async def start_smm():
    return {1: 1}