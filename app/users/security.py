from datetime import timedelta

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pony.orm import db_session

from app.utils.pydantic_security import *
from app.settings.config import cfg
from app.dependencies import *
from app.db.raw_models import User
from app.utils.utils_of_security import generate_security, basic_login


SECRET_KEY = cfg.get('keys', "user")
ACCESS_TOKEN_TIME = int(cfg.get('keys', "user_time"))
token_path = "user_token"
# user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)
[get_user,
 authenticate_user,
 get_current_user,
 create_user_access_token
 ] = generate_security(User)

user = APIRouter(
    tags=["user"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)


@user.post('/' + token_path, response_model=Token)
@db_session
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.scopes:
        form_data.scopes = set(form_data.scopes.append("user"))
    else:
        form_data.scopes = ["user"]
    return basic_login(form_data,
                       authenticate=authenticate_user,
                       access_token_time=ACCESS_TOKEN_TIME,
                       create_access_token=create_user_access_token)


@user.get("/user", response_class=HTMLResponse)
async def login_user(request: Request):
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "участника", "auth_url": '/' + token_path})

