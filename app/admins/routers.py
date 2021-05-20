from typing import Callable
import time

from fastapi import APIRouter, Depends, Security, Response, Request
from pony.orm import db_session

from app.dependencies import *
from app.admins.security import get_current_admin
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB
from fastapi.routing import APIRoute
from app.utils.jinja2_utils import admin_templates, db_templates
from app.pydantic_models import output_ent as out_pd
from app.db import models as m


# class TimedRoute(APIRoute):
#     def get_route_handler(self) -> Callable:
#         original_route_handler = super().get_route_handler()
#
#         async def custom_route_handler(request: Request) -> Response:
#             before = time.time()
#             response: Response = await original_route_handler(request)
#             duration = time.time() - before
#             response.headers["X-Response-Time"] = str(duration)
#             print(f"route duration: {duration}")
#             print(f"route response: {response}")
#             print(f"------------------------route response headers: {response.headers}")
#             print(response.body)
#             return response
#
#         return custom_route_handler


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


@admin.get("/me")
@db_session
def read_users_me(response: Response, request: Request, current_user: HumanInDB = Security(get_current_admin, scopes=["admin"])):
    # print(response)
    return admin_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "Admin_form.html", {"request": request,
                                        "developer": out_pd.Admin(**current_user.dict()),
                                        "action_url": f"/db/Admin/look/",
                                        "send_method": "POST",
                                        "disabled": True,
                                        'access_mode': 'look',
                                        "db_mode": False})
        })


@admin.get("/add_admin")
@db_session
def read_users_me(response: Response, request: Request, current_user: HumanInDB = Security(get_current_admin, scopes=["admin"])):
    print(response)
    return admin_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template("show_entity.html",
                                                              {"request": request,
                                                               "table": m.Admin.get_entities_html(),
                                                               "access": ["admin"]})
        })
# db_templates.TemplateResponse(f"{class_entity_name.value}_form.html", {"request": request, 'access_mode': 'create'})



@admin.get("/me/items/")
@db_session
def read_own_items(current_user: HumanInDB = Security(get_current_admin, scopes=["admin"])):
    return {"item_id": "Foo", "owner": current_user.username}

