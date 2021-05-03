from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.smmers.security import get_current_smmer
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB


smm = APIRouter(
    prefix="/smm",
    tags=["smm"],
    dependencies=[Depends(open_db_session), Depends(get_current_smmer)],  #
    responses={404: {"description": "Not found"}},
)


@smm.get('/')
async def start_smm():
    return {1: 1}