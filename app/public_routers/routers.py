from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pony.orm import db_session

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.dependencies import *
from app.db import models as m
from app.pydantic_models import db_models as pd
from app.pydantic_models import output_ent as out_pd
from app.pydantic_models import simple_entities as easy_ent_pd
from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.utils.jinja2_utils import public_templates
from app.utils.html_utils import Alert


public_router = APIRouter()


@public_router.get('/')
@db_session
def start_public_router(request: Request):
    return public_templates.TemplateResponse("main.html", {
        "request": request,
        "partner": [easy_ent_pd.Partner(id=key, **val) for key, val in dict(m.SimpleEntity['partner'].data).items()],
        "socials": [easy_ent_pd.Socials(id=key, **val) for key, val in dict(m.SimpleEntity['socials'].data).items()],
        "graduates": [out_pd.User.from_pony_orm(i) for i in m.User.select(lambda i: i.visible_about_program_field)[:]]
    })


# @public_router.get('/content/public/{file_path:path}')
# async def get_public_files(file_path: str):
#     file_path = os_join("content", "public", file_path)
#     return FileResponse(file_path)


@public_router.post('/test_auto_pd_human')
async def test_pd(pd_model: pd.Human):
    return pd_model


@public_router.get('/test_jinja', response_class=HTMLResponse)
async def start_public_router(request: Request):
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "Редактораdffffffffffff", "auth_url": '/' + "token_path"})
