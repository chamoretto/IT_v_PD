from typing import Any

from fastapi import APIRouter, Security, Request, status, Path, Body
from fastapi.responses import JSONResponse
from pony.orm import db_session, commit
from pony.orm.dbapiprovider import IntegrityError
from pydantic import create_model

from app.db import models as m
from app.pydantic_models.gen import all_optional_models as op_pd
from app.pydantic_models.gen import output_ent as out_pd
from app.pydantic_models.gen import input_ent as inp_pd
from app.pydantic_models.gen import unique_db_field_models as pk_pd
from app.pydantic_models.gen import only_primarykey_fields_model as only_pk
from app.pydantic_models.gen import db_models_for_create as pd
from app.pydantic_models.gen import db_models as pd_db


from app.pydantic_models.standart_methhods_redefinition import get_pd_class, AccessType, AccessMode, BaseModel
from app.utils.jinja2_utils import db_templates
from app.developers.security import get_current_dev
from app.utils.utils_of_security import get_password_hash
from app.db_router.security import get_current_human_for_db
from app.pydantic_models import gen as role_m
from app.utils.exceptions import ChildHTTPException as HTTPException
from app.utils.responses import RedirectResponseWithBody
from app.pydantic_models.response_models import Ajax300Answer
from app.utils.html_utils import Alert


db_route = APIRouter(
    # route_class=TimedRoute,
    prefix="/db",
    tags=["DataBase"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_human_for_db)
    ],  #
    responses={404: {"description": "Not found------"},
               401: {"description": "Пользователь не был авторизировани"}},

)


# DynamicEnum = enum.Enum('DynamicEnum', {'foo':42, 'bar':24})
# DynamicEnum = enum.Enum('DynamicEnum', {key: key for key, val in m.db.entities.items()})


@db_route.get('/')
@db_session
def all_entities(request: Request, me=Security(get_current_dev, scopes=[str(AccessType.DEVELOPER)])):
    return db_templates.TemplateResponse(
        "main_db.html", {"request": request, "entities": m.db.entities})


@db_route.get('/{entity}')
@db_session
def entity_screen(request: Request,
                  me=Security(get_current_dev, scopes=[str(AccessType.DEVELOPER)]),
                  entity: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")):
    # print("---ESMg mf k", x_part)
    if entity.value not in m.db.entities and type(m.db.entities[entity.value]) == m.db.Entity:
        raise HTTPException(
            request=request,
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Такая Сущность в базе данных не найдена...",
            headers={"WWW-Authenticate": 'Bearer Basic realm="Restricted Area"'},
        )

    return db_templates.TemplateResponse(
        "show_entity.html", {"request": request, **m.db.entities[entity.value].get_entities_html()})


# enum.Enum('DynamicEnum', {key: key for key, val in m.db.entities.items()})


@db_route.get('/{class_entity_name}/new')
@db_session
def entity_screen(request: Request,
                  human=Security(get_current_human_for_db),
                  class_entity_name: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")):

    return db_templates.TemplateResponse(f"{class_entity_name.value}_form.html", {
        "request": request,
        'access_mode': str(AccessMode.CREATE),
        "access": human.scopes
    })


@db_route.post('/{class_entity_name}/new')
@db_session
def create_entity(request: Request,
                  new_ent_data: dict[str, Any] = Body(..., title="Данные нового объекта в базе данных"),
                  human=Security(get_current_human_for_db),
                  class_entity_name: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")
                  ):
    name = class_entity_name.value
    new_ent_data = get_pd_class(name, request, human.scopes, AccessMode.CREATE)(**new_ent_data)
    ent = m.db.entities[name]
    try:
        data = dict(getattr(pk_pd, name)(**dict(new_ent_data)))
    except ImportError as e:
        print('ошибка в create_entity', __file__, "при сохранении созданной сущноси", e)
        raise e
    chek_unique = {key: val for key, val in data.items() if ent.exists(**{key: val})}
    print('chek_unique', chek_unique)
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
        return RedirectResponseWithBody(f"/db/{name}", Ajax300Answer(
            url=f"/db/{name}",
            alert=Alert("Новый объект успешно создан!"),
            request=request))

    except IntegrityError as e:
        print(e)
        if str(e).startswith("UNIQUE constraint failed:"):
            param = str(e).split()[-1].strip('.')[-1]
            return JSONResponse({"answer_for_user": "следующие поля уже существуют",
                                 "type": "fields_no_unique",
                                 "errors": {name + "_" + param + "_error": "этот параметр должен быть уникальным"}
                                 }, status_code=400)
    except Exception as e:
        print("возникла непредвиденная ошибка в", __file__, "create_entity", e, [e])
        return JSONResponse(
            {"answer_for_user": "Возникла непонятная ошибка, попробуйте еще раз",
             "type": "fields_create_entity"}, status_code=400)


@db_route.post('/{class_entity_name}/edit')
@db_session
def edit_entity(
        request: Request,
        human: pd_db.Human = Security(get_current_human_for_db),
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
        pd_entity: BaseModel = get_pd_class(name, request, human.scopes, AccessMode.EDIT).from_pony_orm(entity)
        if getattr(only_pk, name)(**human.dict()).dict() == ent_model.dict():
            human.scopes += [AccessType.SELF]
        return db_templates.TemplateResponse(
            f"{name}_form.html", {"request": request,
                                  name.lower(): pd_entity,
                                  "action_url": f"/db/{name}/edit/save?{entity.key_as_part_query()}",
                                  "send_method": "POST",
                                  'access_mode': 'edit',
                                  "access": human.scopes,
                                  # "entity_primary_keys":
                                  })
    raise HTTPException(
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Сущность для редактирования в базе данных не найдена..."
    )


@db_route.post('/{class_entity_name}/edit/save')
@db_session
def save_edited_entity(
        request: Request,
        human=Security(get_current_human_for_db),
        new_ent_data: dict[str, Any] = Body(..., title="данные, которые требуется изменить в объектк базы данных"),
        class_entity_name: m.db.EntitiesEnum = Path(..., title="Название сущности в базе данных")
):
    # print("query", dict(request.query_params))
    print(human.scopes)
    name = class_entity_name.value
    class_entity = m.db.entities[name]
    old_ent_model = getattr(only_pk, name)(**request.query_params)
    # new_ent_data = getattr(op_pd, name)(**new_ent_data)
    model = get_pd_class(name, request, human.scopes, AccessMode.EDIT)
    print(model)
    print(model.__fields__)
    new_ent_data = model(**new_ent_data)
    print(new_ent_data.dict(exclude_unset=True))
    if class_entity.exists(**old_ent_model.dict(exclude_unset=True)):
        entity = class_entity.get(**old_ent_model.dict(exclude_unset=True))
        try:
            entity.set(**new_ent_data.dict(exclude_unset=True))
            commit()
            return RedirectResponseWithBody(f"/db/{name}", Ajax300Answer(
                url=f"/db/{name}",
                alert=Alert("Объект базы данных отредактирован успешно!", Alert.SUCCESS),
                request=request))
            # return JSONResponse(
            #     {"answer_for_user": "Объект базы данных отредактирован успешно!",
            #      "type": "success edit"}, status_code=201)
        except IntegrityError as e:
            print("Ошибка в save_edited_entity", __file__, e)
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
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Сущность для редактирования в базе данных не найдена..."
    )


@db_route.post('/{class_entity_name}/look')
@db_session
def look_entity(
        request: Request,
        human=Security(get_current_human_for_db),
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
        if getattr(only_pk, name)(**human.dict()).dict() == ent_model.dict():
            human.scopes += [AccessType.SELF]
        return db_templates.TemplateResponse(
            f"{name}_form.html", {"request": request, name.lower(): pd_entity,
                                  # "action_url": f"/db/{name}/look/",
                                  # "send_method": "POST",
                                  # "disabled": True,
                                  'access_mode': 'look',
                                  "access": human.scopes,
                                  })
    raise HTTPException(
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Сущность для редактирования в базе данных не найдена..."
    )


@db_route.post('/{class_entity_name}/delete')
@db_session
def delete_entity(
        request: Request,
        human=Security(get_current_human_for_db),
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
        if getattr(only_pk, name)(**human.dict()).dict() == ent_model.dict():
            human.scopes += [AccessType.SELF]
        entity.delete()
        return RedirectResponseWithBody(f"/db/{name}", Ajax300Answer(
            url=f"/db/{name}",
            alert=Alert("Удаление произошло успешно!", Alert.SUCCESS),
            request=request))
    raise HTTPException(
        request=request,
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Сущность для редактирования в базе данных не найдена..."

    )
