from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import APIRouter, Request, Header
from fastapi.responses import HTMLResponse, JSONResponse
from pony.orm import db_session

from app.utils.pydantic_security import *
from app.settings.config import cfg
from app.dependencies import *
from app.db import models as m
from app.utils.utils_of_security import generate_security, basic_login, scopes_to_db
from app.utils.jinja2_utils import _roles_to_home_urls


SECRET_KEY = cfg.get('keys', "developer")
ACCESS_TOKEN_TIME = int(cfg.get('keys', "developer_time"))
token_path = "developer_token"
# dev_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)
[get_dev,
 authenticate_dev,
 get_current_dev,
 create_dev_access_token] = generate_security(m.Developer)

dev = APIRouter(
    tags=["developer"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)


@dev.post("/" + token_path, response_model=Token)
@db_session
def login_for_access_token_developer(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.scopes:
        form_data.scopes = set(form_data.scopes.extend(scopes_to_db[m.Developer]))
    else:
        form_data.scopes = scopes_to_db[m.Developer]
    form_data.scopes = scopes_to_db[m.Developer]
    return basic_login(request, form_data, access_token_time=ACCESS_TOKEN_TIME)


@dev.get("/dev")
async def login_dev(request: Request):
    print(request.headers)
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "Разработчика", "auth_url": "/" + token_path, "roles_to_home_urls": _roles_to_home_urls})

