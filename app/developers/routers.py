from fastapi import APIRouter, Depends, HTTPException, Security
from pony.orm import db_session

from app.dependencies import *
from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.developers.security import get_current_dev
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB


dev = APIRouter(
    prefix="/dev",
    tags=["developer"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_dev, scopes=["developer"])
    ],  #
    responses={404: {"description": "Not found"}},
)


@dev.get('/some')
async def start_dev():
    return {1: 1}