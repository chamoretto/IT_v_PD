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
from app.db.raw_models import Developer
from app.utils.utils_of_security import generate_security


SECRET_KEY = cfg.get('keys', "developer")
ACCESS_TOKEN_TIME = int(cfg.get('keys', "developer_time"))
token_path = "developer_token"
dev_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)
[get_dev,
 authenticate_dev,
 get_current_dev,
 create_dev_access_token] = generate_security(dev_oauth2_scheme, SECRET_KEY, Developer)

dev = APIRouter(
    tags=["developer"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)


@dev.post("/" + token_path, response_model=Token)
@db_session
def login_for_access_token_developer(form_data: OAuth2PasswordRequestForm = Depends()):
    dev = authenticate_dev(form_data.username, form_data.password)
    if not dev:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_TIME)
    access_token = create_dev_access_token(
        data={"sub": dev.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@dev.get("/dev", response_class=HTMLResponse)
async def login_dev(request: Request):
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "Разработчика", "auth_url": "/" + token_path})

