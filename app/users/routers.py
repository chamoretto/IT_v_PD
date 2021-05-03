from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel


user = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@user.get('/')
async def start_user():
    return {1: 1}