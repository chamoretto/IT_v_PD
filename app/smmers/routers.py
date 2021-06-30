from fastapi import APIRouter, Depends, HTTPException, Security

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.smmers.security import get_current_smmer
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB
from pony.orm import db_session
from app.db import models as m
from app.pydantic_models.standart_methhods_redefinition import AccessType
from fastapi import APIRouter, Security, Response, Request
from pony.orm import db_session

from app.admins.security import get_current_admin
from app.utils.pydantic_security import HumanInDB
from app.utils.jinja2_utils import db_templates, smm_templates
from app.pydantic_models.gen import output_ent as out_pd
from app.db import models as m
from app.pydantic_models.gen import db_models as pd_db
from app.pydantic_models.standart_methhods_redefinition import AccessType, AccessMode


smm = APIRouter(
    prefix="/smm",
    tags=["smm"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_smmer, scopes=[str(AccessType.SMMER)])
    ],  #
    responses={404: {"description": "Not found"}},
)


@smm.get("/me")
def read_users_me(
    response: Response,
    request: Request,
    current_user: pd_db.Human = Security(get_current_smmer, scopes=[str(AccessType.SMMER)]),
):
    print("current_user.dict^ ", type(current_user), current_user)
    print(dict(current_user))
    current_user.scopes += [str(AccessType.SELF)]
    return smm_templates.TemplateResponse(
        "personal_page.html",
        {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "Smm_form.html",
                {
                    "request": request,
                    "smm": out_pd.Smm(**(dict(current_user))),
                    "access": current_user.scopes,
                    "access_mode": AccessMode.LOOK,
                    "db_mode": False,
                },
            ),
        },
    )


@smm.get("/add_event")
@db_session
def read_users_me(
    response: Response,
    request: Request,
    current_user: pd_db.Human = Security(get_current_smmer, scopes=[str(AccessType.SMMER)]),
):
    print(response)
    return smm_templates.TemplateResponse(
        "personal_page.html",
        {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {
                    "request": request,
                    **m.Page.get_entities_html(db_mode=False, access=current_user.scopes),
                },
            ),
        },
    )


@smm.get("/add_news")
@db_session
def read_users_me(
    response: Response,
    request: Request,
    current_user: pd_db.Human = Security(get_current_smmer, scopes=[str(AccessType.SMMER)]),
):
    print(response)
    return smm_templates.TemplateResponse(
        "personal_page.html",
        {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {
                    "request": request,
                    **m.News.get_entities_html(db_mode=False, access=current_user.scopes),
                },
            ),
        },
    )


@smm.get("/look_question")
@db_session
def read_users_me(
    response: Response,
    request: Request,
    current_user: pd_db.Human = Security(get_current_smmer, scopes=[str(AccessType.SMMER)]),
):
    print(response)
    return smm_templates.TemplateResponse(
        "personal_page.html",
        {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {
                    "request": request,
                    **m.Question.get_entities_html(db_mode=False, access=current_user.scopes),
                },
            ),
        },
    )
