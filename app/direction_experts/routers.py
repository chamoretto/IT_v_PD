from fastapi import APIRouter, Depends, HTTPException, Security
from pony.orm import db_session

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.direction_experts.security import get_current_direction_expert
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB
from app.db import models as m
from app.pydantic_models.standart_methhods_redefinition import AccessType

direction_expert = APIRouter(
    prefix="/direction_expert",
    tags=["direction_expert"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_direction_expert, scopes=[str(AccessType.DIRECTION_EXPERT)])],  #
    # responses={404: {"description": "Not found"}},
    # default_response_class=FileResponse
)


@direction_expert.get('/test')
async def start_direction_experts():
    return {1: 1}


@direction_expert.get("/me/", response_model=HumanInDB)
def read_users_me(current_user: HumanInDB = Security(get_current_direction_expert, scopes=[str(AccessType.DIRECTION_EXPERT)])):
    return current_user


@direction_expert.get("/me/items/")
def read_own_items(current_user: HumanInDB = Security(get_current_direction_expert, scopes=[str(AccessType.DIRECTION_EXPERT)])):
    return {"item_id": "Foo", "owner": current_user.username}
