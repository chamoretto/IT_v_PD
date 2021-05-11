from typing import Callable, Any
import time
import enum
from typing import Optional, Set, Union
from functools import wraps
from functools import partial

from fastapi import APIRouter, Depends, Security, Response, Request, HTTPException, status, Path, Form, Body, Header, \
    Query
from fastapi.responses import HTMLResponse, JSONResponse
from pony.orm import db_session, commit
from pydantic import Json
from pony.orm.dbapiprovider import IntegrityError

from fastapi.routing import APIRoute

from app.db import models as m
from app.pydantic_models import db_models as pd
from app.pydantic_models import unique_db_field_models as pk_pd
from app.pydantic_models import input_ent as inp_pd
from app.pydantic_models import output_ent as out_pd
from app.pydantic_models import only_primarykey_fields_model as only_pk
from app.pydantic_models import all_optional_models as op_pd
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
               401: {"description": "Пользователь не был авторизировани"}}, )


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
                  entity: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")):
    # print("---ESMg mf k", x_part)
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


@db_route.get('/{class_entity_name}/new')
@db_session
def entity_screen(request: Request,
                  class_entity_name: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")):
    print("---ESMg mf k")
    if class_entity_name.value not in m.db.entities and type(m.db.entities[class_entity_name.value]) == m.db.Entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такая Сущность в базе данных не найдена...",
            headers={"WWW-Authenticate": 'Bearer Basic realm="Restricted Area"'},
        )

    return db_templates.TemplateResponse(f"{class_entity_name.value}_form.html", {"request": request})


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

@db_route.post('/{class_entity_name}/new')
@db_session
def create_entity(request: Request,
                  new_ent_data:  dict[str, Any] = Body(..., title="Данные нового объекта в базе данных"),
                  class_entity_name: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")
                  ):

    name = class_entity_name.value
    new_ent_data = getattr(inp_pd, name)(**new_ent_data)
    ent = m.db.entities[name]

    data = dict(getattr(pk_pd, name)(**dict(new_ent_data))).items()
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
    new_ent_data = getattr(op_pd, name)(**dict(new_ent_data), hash_password=password)
    try:
        ent(**dict(new_ent_data))
        commit()
        return JSONResponse({"answer_for_user": "Данные успешно внесены в базу данных",
                             "type": "success_creation"}, status_code=201)
    except IntegrityError as e:
        print(e)
        if str(e).startswith("UNIQUE constraint failed:"):
            param = str(e).split()[-1].strip('.')[-1]
            return JSONResponse({"answer_for_user": "следующие поля уже существуют",
                                 "type": "fields_no_unique",
                                 "errors": {name + "_" + param + "_error": "этот параметр должен быть уникальным"}
                                 }, status_code=400)
    except Exception as e:
        print("возникла непредвиденная ошибка в", __file__, "create_entity", e)
        return JSONResponse(
            {"answer_for_user": "Возникла непонятная ошибка, попробуйте еще раз",
             "type": "fields_create_entity"}, status_code=400)


@db_route.post('/{class_entity_name}/edit')
@db_session
def edit_entity(
        request: Request,
        ent_model: dict[str, Any] = Body(
            ...,
            title="словарь, однозначно определяющий объект в БД, через задание всех primaryKey"
                  " (если их несколько)",
            description="словарь из пар <key, value> где key - имя primaryKey объекта в БД,"
                        "а value - значение primaryKey конкретной сущности"),
        class_entity_name: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")
):
    name = class_entity_name.value
    ent_model = getattr(only_pk, name)(**ent_model)
    class_entity = m.db.entities[name]
    if class_entity.exists(**dict(ent_model)):
        entity = class_entity.get(**dict(ent_model))
        pd_entity = getattr(out_pd, name).from_pony_orm(entity)
        return db_templates.TemplateResponse(
            f"{name}_form.html", {"request": request, name.lower(): pd_entity,
                                  "action_url": f"/db/{name}/edit/save?{entity.key_as_part_query()}",
                                  "send_method": "POST"})
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Сущность для редактирования в базе данных не найдена..."
    )


@db_route.post('/{class_entity_name}/edit/save')
@db_session
def save_edited_entity(
        request: Request,
        new_ent_data: dict[str, Any] = Body(..., title="данные, которые требуется изменить в объектк базы данных"),
        class_entity_name: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")
):
    print("query", dict(request.query_params))
    name = class_entity_name.value
    class_entity = m.db.entities[name]
    old_ent_model = getattr(only_pk, name)(**request.query_params)
    new_ent_data = getattr(op_pd, name)(**new_ent_data)
    if class_entity.exists(**old_ent_model.dict(exclude_unset=True)):
        entity = class_entity.get(**old_ent_model.dict(exclude_unset=True))
        try:
            entity.set(**new_ent_data.dict(exclude_unset=True))
            commit()
            return JSONResponse(
                {"answer_for_user": "Объект базыданных отредактирован успешно!",
                 "type": "success edit"}, status_code=201)
        except IntegrityError as e:
            print(e)
            if str(e).startswith("UNIQUE constraint failed:"):
                param = str(e).split()[-1].strip('.')[-1]
                return JSONResponse({"answer_for_user": "следующие поля уже существуют",
                                     "type": "fields_no_unique",
                                     "errors": {name + "_" + param + "_error": "этот параметр должен быть уникальным"}
                                     }, status_code=400)
        except Exception as e:
            print("возникла непредвиденная ошибка в", __file__, "save_edited_entity", e)
            return JSONResponse(
                {"answer_for_user": "Возникла непонятная ошибка, попробуйте еще раз",
                 "type": "fields_create_entity"}, status_code=400)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Сущность для редактирования в базе данных не найдена..."
    )


@db_route.post('/{class_entity_name}/look')
@db_session
def look_entity(
        request: Request,
        ent_model: dict[str, Any] = Body(
            ...,
            title="словарь, однозначно определяющий объект в БД, через задание всех primaryKey"
                  " (если их несколько)",
            description="словарь из пар <key, value> где key - имя primaryKey объекта в БД,"
                        "а value - значение primaryKey конкретной сущности"),
        class_entity_name: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")
):
    name = class_entity_name.value
    ent_model = getattr(only_pk, name)(**ent_model)
    class_entity = m.db.entities[name]
    if class_entity.exists(**dict(ent_model)):
        entity = class_entity.get(**dict(ent_model))
        pd_entity = getattr(out_pd, name).from_pony_orm(entity)
        return db_templates.TemplateResponse(
            f"{name}_form.html", {"request": request, name.lower(): pd_entity,
                                  "action_url": f"/db/{name}/look/",
                                  "send_method": "POST",
                                  "disabled": True})
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Сущность для редактирования в базе данных не найдена..."
    )

@db_route.post('/{class_entity_name}/delete')
@db_session
def delete_entity(
        request: Request,
        ent_model: dict[str, Any] = Body(
            ...,
            title="словарь, однозначно определяющий объект в БД, через задание всех primaryKey"
                  " (если их несколько)",
            description="словарь из пар <key, value> где key - имя primaryKey объекта в БД,"
                        "а value - значение primaryKey конкретной сущности"),
        class_entity_name: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")
):
    name = class_entity_name.value
    ent_model = getattr(only_pk, name)(**ent_model)
    class_entity = m.db.entities[name]
    if class_entity.exists(**dict(ent_model)):
        entity = class_entity.get(**dict(ent_model))
        entity.delete()
        return {"redirect": ""}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Сущность для редактирования в базе данных не найдена..."
    )

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
