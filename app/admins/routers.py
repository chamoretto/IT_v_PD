from fastapi import APIRouter, Security, Response, Request
from pony.orm import db_session

from app.admins.security import get_current_admin
from app.utils.pydantic_security import HumanInDB
from app.utils.jinja2_utils import admin_templates, db_templates
from app.pydantic_models.gen import output_ent as out_pd
from app.db import models as m
from app.pydantic_models.gen import db_models as pd_db



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
def read_users_me(response: Response,
                  request: Request,
                  current_user: pd_db.Human = Security(get_current_admin, scopes=["admin"])):
    print("current_user.dict^ ", type(current_user), current_user)
    print(dict(current_user))
    return admin_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "Admin_form.html", {"request": request,
                                        "admin": out_pd.Admin(**(dict(current_user))),
                                        # "action_url": f"/db/Admin/look/",
                                        # "send_method": "POST",
                                        # "disabled": True,
                                        'access_mode': 'look',
                                        "db_mode": False})
        })


@admin.get("/add_admin")
@db_session
def read_users_me(response: Response,
                  request: Request,
                  current_user: pd_db.Human = Security(get_current_admin, scopes=["admin"])):
    print(response)
    return admin_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {"request": request,
                 **m.Admin.get_entities_html(db_mode=False, access=["admin"]),
                 })
        })


@admin.get("/add_smm")
@db_session
def read_users_me(response: Response,
                  request: Request,
                  current_user: pd_db.Human = Security(get_current_admin, scopes=["admin"])):
    print(response)
    return admin_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {"request": request,
                 **m.Smm.get_entities_html(db_mode=False, access=["admin"]),
                 })
        })

@admin.get("/add_expert")
@db_session
def read_users_me(response: Response,
                  request: Request,
                  current_user: pd_db.Human = Security(get_current_admin, scopes=["admin"])):
    print(response)
    return admin_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {"request": request,
                 **m.DirectionExpert.get_entities_html(db_mode=False, access=["admin"]),
                 })
        })


@admin.get("/add_event")
@db_session
def read_users_me(response: Response,
                  request: Request,
                  current_user: pd_db.Human = Security(get_current_admin, scopes=["admin"])):
    print(response)
    return admin_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {"request": request,
                 **m.Page.get_entities_html(db_mode=False, access=["admin"]),
                 })
        })


@admin.get("/add_news")
@db_session
def read_users_me(response: Response,
                  request: Request,
                  current_user: pd_db.Human = Security(get_current_admin, scopes=["admin"])):
    print(response)
    return admin_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {"request": request,
                 **m.News.get_entities_html(db_mode=False, access=["admin"]),
                 })
        })


@admin.get("/look_question")
@db_session
def read_users_me(response: Response,
                  request: Request,
                  current_user: pd_db.Human = Security(get_current_admin, scopes=["admin"])):
    print(response)
    return admin_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {"request": request,
                 **m.Question.get_entities_html(db_mode=False, access=["admin"]),
                 })
        })


@admin.get("/me/items/")
@db_session
def read_own_items(current_user: pd_db.Human = Security(get_current_admin, scopes=["admin"])):
    return {"item_id": "Foo", "owner": current_user.username}

