from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.users.security import get_current_user
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB


user = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(open_db_session), Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@user.get('/')
async def start_user():
    return {1: 1}