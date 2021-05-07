from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from pony.orm import db_session

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.dependencies import *
from app.pydantic_models import db_models as pd
from app.pydantic_models.standart_methhods_redefinition import BaseModel


public_router = APIRouter()


@public_router.get('/')
async def start_public_router():
    return {1: 1}


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
