from fastapi import APIRouter, Security, Response, Request
from pony.orm import db_session

from app.admins.security import get_current_admin
from app.utils.pydantic_security import HumanInDB
from app.utils.jinja2_utils import admin_templates, db_templates
from app.pydantic_models.gen import output_ent as out_pd
from app.db import models as m
from app.pydantic_models.gen import db_models as pd_db


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
                                        "db_mode": False,})
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
                 **m.Admin.get_entities_html(db_mode=False, access=current_user.scopes),
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
                 **m.Smm.get_entities_html(db_mode=False, access=current_user.scopes),
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
                 **m.DirectionExpert.get_entities_html(db_mode=False, access=current_user.scopes),
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
                 **m.Page.get_entities_html(db_mode=False, access=current_user.scopes),
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
                 **m.News.get_entities_html(db_mode=False, access=current_user.scopes),
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
                 **m.Question.get_entities_html(db_mode=False, access=current_user.scopes),
                 })
        })

