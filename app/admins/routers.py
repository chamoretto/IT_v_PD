from fastapi import APIRouter, Depends

from app.dependencies import *
from app.admins.security import get_current_admin
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB


admin = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(open_db_session), Depends(get_current_admin)], #
    # responses={404: {"description": "Not found"}},
    # default_response_class=FileResponse
)


@admin.get('/test')
async def start_admin():
    return {1: 1}


@admin.get("/me/", response_model=HumanInDB)
def read_users_me(current_user: HumanInDB = Depends(get_current_admin)):
    return current_user


@admin.get("/me/items/")
def read_own_items(current_user: HumanInDB = Depends(get_current_admin)):
    return {"item_id": "Foo", "owner": current_user.username}