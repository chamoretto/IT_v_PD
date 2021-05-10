# -*- coding: utf-8 -*-

"""Главный файл нашего web-приложения"""

import uvicorn
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import StreamingResponse
from pony.orm.core import TransactionIntegrityError

from app.dependencies import *
from app.public_routers.routers import public_router
from app.users.routers import user
from app.smmers.routers import smm
from app.admins.routers import admin
from app.developers.routers import dev
from app.direction_experts.routers import direction_expert
from app.users.security import user as security_user
from app.smmers.security import smmer as security_smmer
from app.direction_experts.security import direction_expert as security_direction_expert
from app.admins.security import admin as security_admin
from app.developers.security import dev as security_dev
from app.utils.utils_of_security import security
from app.utils.basic_utils import async_iterator_wrapper as aiwrap
from app.utils.html_utils import Alert
from app.db.create_db_content import create_pages
from app.db_router.routers import db_route

app = FastAPI(
    # route_class=TimedRoute,
)
# app.add_middleware(HTTPSRedirectMiddleware)  # Устанавливаем https
# app.add_middleware(GZipMiddleware, minimum_size=1000)  # все файлы ответов больше 1000 байт сжимаются


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     response: StreamingResponse = await call_next(request)
#     # print("---==!!", response.headers)
#     if any(["text/html" in val.lower() for key, val in response.headers.items() if key.lower() == "content-type"]):
#         resp_body = [section async for section in response.__dict__['body_iterator']]
#         # print(resp_body)
#         # print(hasattr(response, "template"))
#         response.__setattr__('body_iterator', aiwrap(resp_body))
#         return response
#     # content = await response.body_iterator
#     # response.body_iterator = (content)
#     # print(type(response), content)
#     # await response("", receive, send)
#     return response


app.mount("/public", StaticFiles(directory="content/public"), name="public")
app.mount("/static", StaticFiles(directory="content/static"), name="static")
app.mount("/scripts", StaticFiles(directory="content/scripts"), name="scripts")
app.mount("/stiles", StaticFiles(directory="content/stiles"), name="stiles")
app.mount("/fonts", StaticFiles(directory="content/fonts"), name="fonts")
app.mount("/docs", StaticFiles(directory="content/public/docs"), name="docs")
app.mount("/img", StaticFiles(directory="content/public/images"), name="img")

app.include_router(public_router)
app.include_router(user)
app.include_router(smm)
app.include_router(direction_expert)
app.include_router(admin)
app.include_router(dev)
app.include_router(db_route)

app.include_router(security_user)
app.include_router(security_smmer)
app.include_router(security_direction_expert)
app.include_router(security_admin)
app.include_router(security_dev)

app.include_router(security)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/test", response_class=HTMLResponse)
async def root():
    return FileResponse('index.html')


@app.get('/something')
def trololo():
    print("__0))(#)Iw4985")
    return {"aa": "bb"}


@app.get('/gimg')
async def getimg(some_func: str = ""):
    try:
        some_func: str = trololo
        return some_func()
    except Exception:
        return {'1': 1}


@app.exception_handler(StarletteHTTPException)
def custom_http_exception_handler(request: Request, exc: HTTPException):
    try:
        # print(request)
        # print(request.url, request.method)
        # print([exc])
        if exc.status_code == 401:
            return error_templates.TemplateResponse(
                "401.html",
                {
                    "request": request,
                    "current_url": request.url,
                    "current_method": request.method
                },
                status_code=401,
            )

        elif exc.status_code == 404:
            return error_templates.TemplateResponse("404.html", {
                "request": request,
                "detail": exc.detail,
                "alert": Alert("Похоже данной страницы не существует...", Alert.ERROR)})
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": f"Oops! did something. There goes a rainbow..."},
        )
    except Exception as e:
        print("-------------", e)
        return "help me!"


# from fastapi import Depends, FastAPI
# from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from passlib.context import CryptContext
# from datetime import datetime, timedelta
# from typing import Optional, Callable, Any
# from pydantic import ValidationError
#
# from fastapi import Depends, HTTPException, status, APIRouter
# from jose import JWTError, jwt
# from pony.orm import db_session
# from fastapi.security import (
#     OAuth2PasswordBearer,
#     OAuth2PasswordRequestForm,
#     SecurityScopes,
# )
# from app.db import raw_models as models
# from app.settings.config import cfg
# from app.utils.pydantic_security import TokenData, HumanInDB, Token
# from app.utils.utils_of_security import check_scopes, basic_create_access_token
#
# app = FastAPI()
#
# security = HTTPBasic()
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="token",
#     scopes={
#         "user": "Участник программы 1000ln",
#         "smmer": "Редактор различного контента на сайте",
#         "direction_expert": "Проверяющий работы на конкурсе",
#         "admin": "Управляющий сайтом",
#         "developer": "Разработчик сайта"
#     },
# )
#
# @app.get("/users/me")
# def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
#     return {"username": credentials.username, "password": credentials.password}
#
#
# @app.get("/token")
# @db_session
# def basic_login(credentials: HTTPBasicCredentials = Depends(security),
#                 # form_data: OAuth2PasswordRequestForm = Depends(),
#                 authenticate: str = None,
#                 access_token_time=0,
#                 create_access_token: str = None,
#                 scopes: list = []
#
#                 ):
#     try:
#         # form_data = Depends(OAuth2PasswordRequestForm)
#         print(credentials.username, credentials.password,)
#         error = HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": 'Bearer'},
#         )
#         if create_access_token is None and authenticate is None:
#             print(1)
#             role = check_scopes(credentials.username, credentials.password, scopes)
#             if not role or not bool(role):
#                 print(0, role)
#                 raise error
#             role = HumanInDB.from_orm(role[-1])
#             create_access_token = basic_create_access_token
#             access_token_time = 30
#         elif authenticate is None:
#             print(2)
#             raise error
#         elif create_access_token is None:
#             print(3)
#             raise error
#         else:
#             print(4)
#             role = authenticate(credentials.username, credentials.password)
#         if not role:
#             print(5)
#             raise error
#         access_token_expires = timedelta(minutes=access_token_time)
#         access_token = create_access_token(
#             data={"sub": role.username, "scopes": scopes},
#             expires_delta=access_token_expires,
#         )
#         print(scopes, "access_token", access_token)
#         return {"access_token": access_token, "token_type": "bearer"}
#     except Exception as e:
#         print("--------------------------", [e])
#         return {"username": credentials.username, "password": credentials.password}


if __name__ == "__main__":
    try:
        create_pages()
    except TransactionIntegrityError:
        pass
    # with db_session:
    #     print(Human.get(username="developer").__class__)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
