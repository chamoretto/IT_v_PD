from fastapi import APIRouter, Depends, Security, Response, Request
from pony.orm import db_session

from app.dependencies import *
from app.admins.security import get_current_admin
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB

admin = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_admin, scopes=["admin"])
    ],  #
    responses={404: {"description": "Not found------"},
               401: {"description": "Пользователь не был авторизировани"}},
)


@admin.get('/test')
@db_session
async def start_admin():
    return {1: 1}


@admin.get("/me/", response_model=HumanInDB)
@db_session
def read_users_me(response: Response, current_user: HumanInDB = Security(get_current_admin, scopes=["admin"])):
    print(response)
    # response.headers["WWW-Authenticate"] = 'Basic realm="Restricted Area"'
    return current_user


@admin.get("/me/items/")
@db_session
def read_own_items(current_user: HumanInDB = Security(get_current_admin, scopes=["admin"])):
    return {"item_id": "Foo", "owner": current_user.username}
