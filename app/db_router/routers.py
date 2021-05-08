from typing import Callable
import time

from fastapi import APIRouter, Depends, Security, Response, Request, HTTPException, status
from pony.orm import db_session


from fastapi.routing import APIRoute

from app.db import models as m
from app.dependencies import *
from app.utils.jinja2_utils import db_templates
from app.developers.security import get_current_dev
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB

db_route = APIRouter(
    # route_class=TimedRoute,
    prefix="/db",
    tags=["DataBase"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_dev, scopes=["developer"])
    ],  #
    responses={404: {"description": "Not found------"},
               401: {"description": "Пользователь не был авторизировани"}},
)


@db_route.get('/{entity}')
async def start_dev(entity: str, request: Request):
    if entity not in m.db.entities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такая Сущность в базе данных не найдена...",
            headers={"WWW-Authenticate": 'Bearer Basic realm="Restricted Area"'},
        )
    return db_templates.TemplateResponse(
        "show_entity.html",
        {"request": request})
