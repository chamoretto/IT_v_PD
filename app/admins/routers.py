from typing import Callable
import time

from fastapi import APIRouter, Depends, Security, Response, Request
from pony.orm import db_session

from app.dependencies import *
from app.admins.security import get_current_admin
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB
from fastapi.routing import APIRoute


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"------------------------route response headers: {response.headers}")
            print(response.body)
            return response

        return custom_route_handler


admin = APIRouter(
    # route_class=TimedRoute,
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
