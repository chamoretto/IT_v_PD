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
from app.utils.utils_of_security import generate_security


SECRET_KEY = cfg.get('keys', "user")
ACCESS_TOKEN_TIME = int(cfg.get('keys', "user_time"))
token_path = "user_token"
user_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)
[get_user,
 authenticate_user,
 get_current_user,
 create_user_access_token
 ] = generate_security(user_oauth2_scheme, SECRET_KEY, User)

user = APIRouter(
    tags=["user"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)


@user.post('/' + token_path, response_model=Token)
@db_session
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_TIME)
    access_token = create_user_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@user.get("/user", response_class=HTMLResponse)
async def login_user(request: Request):
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "участника", "auth_url": '/' + token_path})

