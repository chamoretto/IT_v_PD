from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pony.orm import db_session

from app.utils.pydantic_security import *
from app.settings.config import cfg
from app.dependencies import *
from app.db import models as m
from app.utils.utils_of_security import generate_security, basic_login, scopes_to_db
from app.utils.jinja2_utils import _roles_to_home_urls


SECRET_KEY = cfg.get('keys', "smmer")
ACCESS_TOKEN_TIME = int(cfg.get('keys', "smmer_time"))
token_path = "smmer_token"
# smmer_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)
[get_smmer,
 authenticate_smmer,
 get_current_smmer,
 create_smmer_access_token
 ] = generate_security(m.Smm)

smmer = APIRouter(
    tags=["smm"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)


@smmer.post('/' + token_path, response_model=Token)
@db_session
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.scopes:
        form_data.scopes = set(form_data.scopes.extend(scopes_to_db[m.Smm]))
    else:
        form_data.scopes = scopes_to_db[m.Smm]
    return basic_login(request, form_data, access_token_time=ACCESS_TOKEN_TIME)


@smmer.get("/smm", response_class=HTMLResponse)
async def login_smmer(request: Request):
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "Редактора", "auth_url": '/' + token_path, "roles_to_home_urls": _roles_to_home_urls})
