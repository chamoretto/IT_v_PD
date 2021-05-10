from typing import Callable
import time
import enum
from typing import Optional, Set, Union
from functools import wraps
from functools import partial

from fastapi import APIRouter, Depends, Security, Response, Request, HTTPException, status, Path, Form, Body, Header
from fastapi.responses import HTMLResponse, JSONResponse
from pony.orm import db_session, commit
from pydantic import Json

from fastapi.routing import APIRoute

from app.db import models as m
from app.pydantic_models import db_models as pd
from app.pydantic_models import unique_db_field_models as pk_pd
from app.pydantic_models import input_ent as inp_pd
from app.pydantic_models import output_ent as out_pd
from app.dependencies import *
from app.utils.jinja2_utils import db_templates
from app.developers.security import get_current_dev
from app.utils.utils_of_security import get_password_hash
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB
from app.pydantic_models.standart_methhods_redefinition import BaseModel, as_form
from app.pydantic_models.db_models import OptionalPkHumanContacts, HumanContacts, PkQuestion, SetPkQuestion, \
    OptionalPkQuestion, Question

db_route = APIRouter(
    # route_class=TimedRoute,
    prefix="/db",
    tags=["DataBase"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_dev, scopes=["developer"])
    ],  #
    responses={404: {"description": "Not found------"},
               401: {"description": "Пользователь не был авторизировани"}},)
# DynamicEnum = enum.Enum('DynamicEnum', {'foo':42, 'bar':24})
# DynamicEnum = enum.Enum('DynamicEnum', {key: key for key, val in m.db.entities.items()})
@db_route.get('/')
@db_session
def all_entities(request: Request):
    return db_templates.TemplateResponse(
        "main_db.html", {"request": request, "entities": m.db.entities})


@db_route.get('/{entity}')
@db_session
def entity_screen(request: Request,
                  entity: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных"),
                  x_part: Optional[list[str]] = Header(None)):
    print("---ESMg mf k", x_part)
    if entity.value not in m.db.entities and type(m.db.entities[entity.value]) == m.db.Entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такая Сущность в базе данных не найдена...",
            headers={"WWW-Authenticate": 'Bearer Basic realm="Restricted Area"'},
        )

    return db_templates.TemplateResponse(
        "show_entity.html", {"request": request, "table": m.db.entities[entity.value].get_entities_html()})


# enum.Enum('DynamicEnum', {key: key for key, val in m.db.entities.items()})

"""
        Базовый класс человека

        :param id: Идентификатор
        :type id: number
        :param username: Логин
        :type username: text
        :param name: Имя пользователя
        :type name: text
        :param surname: Фамилия пользователя
        :type surname: text
        :param email: Почта
        :type email: text
        :param status: Почта
        :type status: text
        :param description: Почта
        :type description: text

        напрямую использоваться не должен
    """


@db_route.get('/{entity}/new')
@db_session
def entity_screen(request: Request,
                  entity: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")):
    print("---ESMg mf k")
    if entity.value not in m.db.entities and type(m.db.entities[entity.value]) == m.db.Entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такая Сущность в базе данных не найдена...",
            headers={"WWW-Authenticate": 'Bearer Basic realm="Restricted Area"'},
        )

    return db_templates.TemplateResponse(f"{entity.value}_form.html", {"request": request})
# @as_form
# class TestHuman(BaseModel):
#     id: int
#     username: str
#     hash_password: str
#     name: str = 'Вася'
#     surname: str
#     email: str
#     human_contacts: Union[int, HumanContacts, None] = None
#     photo: Optional[str] = ''
#     status: Optional[str] = ''
#     description: Optional[str] = ''
#     scopes: Optional[Json] = "{}"
#     questions: Set[Union[int, Question]] = []
#
#
#     class Config:
#         orm_mode = True

# def check(entity: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных"), )
def simple_decorator(name, ent):

    def create_entity(request: Request,
                      new_ent_data: getattr(inp_pd, name) = Body(...)):

        data = dict(getattr(pk_pd, name)(**dict(new_ent_data))).items()
        print(data, ent.__name__, name, ent.exists(id=1))
        chek_unique = {key: val for key, val in data if ent.exists(**{key: val})}
        print(chek_unique)
        if bool(chek_unique):
            return JSONResponse(
                {"answer_for_user": "следующие поля уже существуют",
                 "type": "fields_no_unique",
                 "errors": {name + "_" + key + "_error": "Введите другое значение в это поле. Это занято" for key in
                            chek_unique}
                 }, status_code=400)
        password = dict(new_ent_data).get("password")
        if password:
            password = get_password_hash(password)
        new_ent_data = getattr(pd, name)(**dict(new_ent_data), hash_password=password)
        try:
            ent(**dict(new_ent_data))
            commit()
        except Exception as e:
            return JSONResponse(
                {"answer_for_user": "Возникла непонятная ошибка, попробуйте еще раз",
                 "type": "fields_create_entity"}, status_code=400)
        return JSONResponse({"answer_for_user": "Данные успешно внесены в базу данных",
                             "type": "success_creation"}, status_code=201)
    return create_entity


for name, ent in m.db.entities.items():
    create_func = partial(simple_decorator, name=name, ent=ent)()
    create_func = db_session(create_func)
    decorator_maker = db_route.post(f'/{name}/new')
    create_func = decorator_maker(create_func)

# @wraps(entity_screen)
# @db_route.post('/' + name + '/new', status_code=201)
# @db_session

# if True:

# @db_route.post('/Human/new')
# @db_session
# def entity_screen(request: Request, new_ent_data: pd.Human = Body(...)):
#     print(pd.Human, "---!!!!!!!!!!!!!!!!!!!!!", new_ent_data)
#     return new_ent_data


# return db_templates.TemplateResponse(f"{entity.value}_form.html", {"request": request})

# @db_route.post('/Human/new')
# @db_session
# def entity_screen(username: str = Form(None),
#                   name: str = Form(None),
#                   surname: str = Form(None),
#                   email: str = Form(None),
#                   status: str = Form(None),
#                   description: str = Form(None),
#                   ):
#     return {"username": username, "name":name}
