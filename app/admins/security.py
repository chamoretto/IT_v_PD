from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, FileResponse
from jose import jwt
from pony.orm import db_session

from ..utils.utils_of_security import verify_password
from app.utils.pydantic_security import *
from ..settings.config import cfg
from app.dependencies import *
from ..db.raw_models import Admin
from app.db.db_utils import open_db_session
from app.utils.utils_of_security import generate_security


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = cfg.get('keys', "admin")

ACCESS_TOKEN_TIME = int(cfg.get('keys', "admin_time"))


admin = APIRouter(
    tags=["admin"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)

admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin_token")

get_admin, authenticate_admin, get_current_admin, create_admin_access_token = generate_security(admin_oauth2_scheme,
                                                                                                SECRET_KEY,
                                                                                                Admin)

token_path = "/admin_token"


@admin.post(token_path, response_model=Token)
@db_session
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    admin = authenticate_admin(form_data.username, form_data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_TIME)
    access_token = create_admin_access_token(
        data={"sub": admin.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@admin.get("/admin", response_class=HTMLResponse)
async def login_admin(request: Request):
    return login_templates.TemplateResponse("login.html", {"request": request, "who": "Админа", "auth_url": token_path})

