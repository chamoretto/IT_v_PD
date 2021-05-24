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


# SECRET_KEY = cfg.get('keys', "user")
# ACCESS_TOKEN_TIME = int(cfg.get('keys', "user_time"))
token_path = "checking_login_data"
# user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)
[get_human,
 _,
 get_current_human,
 create_user_access_token
 ] = generate_security(m.Human)

public_security = APIRouter(
    tags=["public"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)


@public_security.post('/' + token_path)
@db_session
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    return basic_login(request, form_data, access_token_time=30)


@public_security.get("/log_in")
async def login_user(request: Request):
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "", "auth_url": '/' + token_path})

