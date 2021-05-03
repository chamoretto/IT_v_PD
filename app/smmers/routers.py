from fastapi import APIRouter, Depends, HTTPException, Security

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.smmers.security import get_current_smmer
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB


smm = APIRouter(
    prefix="/smm",
    tags=["smm"],
    dependencies=[Depends(open_db_session),
                  Security(get_current_smmer, scopes=["smmer"])],  #
    responses={404: {"description": "Not found"}},
)


@smm.get('/some')
async def start_smmer():
    return {1: 1}

@smm.get("/me/", response_model=HumanInDB)
def read_users_me(current_user: HumanInDB = Security(get_current_smmer, scopes=["smmer"])):
    return current_user


@smm.get("/me/items/")
def read_own_items(current_user: HumanInDB = Security(get_current_smmer, scopes=["smmer"])):
    return {"item_id": "Foo", "owner": current_user.username}