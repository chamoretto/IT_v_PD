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
from app.db.raw_models import Smm
from app.utils.utils_of_security import generate_security


SECRET_KEY = cfg.get('keys', "smmer")
ACCESS_TOKEN_TIME = int(cfg.get('keys', "smmer_time"))
token_path = "smmer_token"
smmer_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)
[get_smmer,
 authenticate_smmer,
 get_current_smmer,
 create_smmer_access_token
 ] = generate_security(smmer_oauth2_scheme, SECRET_KEY, Smm)

smmer = APIRouter(
    tags=["smm"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)


@smmer.post('/' + token_path, response_model=Token)
@db_session
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    smmer = authenticate_smmer(form_data.username, form_data.password)
    if not smmer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_TIME)
    access_token = create_smmer_access_token(
        data={"sub": smmer.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@smmer.get("/smm", response_class=HTMLResponse)
async def login_smmer(request: Request):
    return login_templates.TemplateResponse(
        "login.html",
        {"request": request, "who": "Редактора", "auth_url": '/' + token_path})
