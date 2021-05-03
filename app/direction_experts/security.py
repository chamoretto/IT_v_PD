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
from app.db.raw_models import DirectionExpert
from app.utils.utils_of_security import generate_security


SECRET_KEY = cfg.get('keys', "direction_expert")
ACCESS_TOKEN_TIME = int(cfg.get('keys', "direction_expert_time"))
token_path = "direction_expert_token"
direction_expert_oauth2_scheme = OAuth2PasswordBearer(tokenUrl=token_path)
[get_direction_expert,
 authenticate_direction_expert,
 get_current_direction_expert,
 create_direction_expert_access_token
 ] = generate_security(direction_expert_oauth2_scheme, SECRET_KEY, DirectionExpert)

direction_expert = APIRouter(
    tags=["direction_expert"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(open_db_session)]
)


@direction_expert.post("/" + token_path, response_model=Token)
@db_session
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    direction_expert = authenticate_direction_expert(form_data.username, form_data.password)
    if not direction_expert:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_TIME)
    access_token = create_direction_expert_access_token(
        data={"sub": direction_expert.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@direction_expert.get("/direction_expert", response_class=HTMLResponse)
async def login_direction_expert(request: Request):
    return login_templates.TemplateResponse(
        "login.html", {"request": request, "who": "Админа", "auth_url": "/" + token_path})
