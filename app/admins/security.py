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
from app.db.raw_models import Admin
from app.utils.utils_of_security import generate_security, basic_login

SECRET_KEY = cfg.get('keys', "admin")
ACCESS_TOKEN_TIME = int(cfg.get('keys', "admin_time"))
token_path = "admin_token"
# admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)

admin = APIRouter(
    tags=["admin"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)

[get_admin,
 authenticate_admin,
 get_current_admin,
 create_admin_access_token
 ] = generate_security(Admin)


@admin.post("/" + token_path, response_model=Token)
@db_session
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.scopes:
        form_data.scopes = set(form_data.scopes.append("admin"))
    else:
        form_data.scopes = ["admin"]
    return basic_login(form_data, access_token_time=ACCESS_TOKEN_TIME)


@admin.get("/admin", response_class=HTMLResponse)
async def login_admin(request: Request):
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "Админа", "auth_url": "/" + token_path})
