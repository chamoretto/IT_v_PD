from fastapi import APIRouter, Depends, HTTPException, Security
from pony.orm import db_session

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.direction_experts.security import get_current_direction_expert
from app.db.db_utils import open_db_session
from app.utils.pydantic_security import HumanInDB
from app.db import models as m
from app.pydantic_models.standart_methhods_redefinition import AccessType
from fastapi import APIRouter, Security, Response, Request
from pony.orm import db_session

from app.admins.security import get_current_admin
from app.utils.pydantic_security import HumanInDB
from app.utils.jinja2_utils import db_templates, expert_templates
from app.pydantic_models.gen import output_ent as out_pd
from app.db import models as m
from app.pydantic_models.gen import db_models as pd_db
from app.pydantic_models.standart_methhods_redefinition import AccessType, AccessMode


direction_expert = APIRouter(
    prefix="/direction_expert",
    tags=["direction_expert"],
    dependencies=[
        # Depends(open_db_session),
        Security(get_current_direction_expert, scopes=[str(AccessType.DIRECTION_EXPERT)])],  #
    # responses={404: {"description": "Not found"}},
    # default_response_class=FileResponse
)


@direction_expert.get("/me")
@db_session
def read_users_me(response: Response,
                  request: Request,
                  current_user: pd_db.Human = Security(get_current_direction_expert, scopes=[str(AccessType.DIRECTION_EXPERT)])):
    print("current_user.dict^ ", type(current_user), current_user)
    print(dict(current_user))
    current_user.scopes += [str(AccessType.SELF)]
    return expert_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "DirectionExpert_form.html", {"request": request,
                                    "directionexpert": out_pd.DirectionExpert(**(dict(current_user))),
                                    "access": current_user.scopes,
                                    'access_mode': AccessMode.LOOK,
                                    "db_mode": False})
        })


@direction_expert.get("/user_works")
@db_session
def get_user_works(response: Response,
                  request: Request,
                  current_user: pd_db.DirectionExpert = Security(get_current_direction_expert, scopes=[str(AccessType.DIRECTION_EXPERT)])):
    return expert_templates.TemplateResponse(
        "personal_page.html", {
            "request": request,
            "personal_data": db_templates.get_cooked_template(
                "show_entity.html",
                {"request": request,
                 **m.UserWork.get_entities_html(db_mode=False, access=current_user.scopes),
                 }
            )
        }
    )