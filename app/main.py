# -*- coding: utf-8 -*-

"""Главный файл нашего web-приложения"""

import uvicorn
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from fastapi import FastAPI, Request, Query, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import StreamingResponse
from pony.orm.core import TransactionIntegrityError, db_session, show

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
from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.db import models as m
from app.utils.jinja2_utils import public_templates
from app.utils.exceptions import ChildHTTPException as HTTPException


app = FastAPI()
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


@app.get("/test", response_class=HTMLResponse)
async def root():
    return FileResponse('index.html')


@app.exception_handler(StarletteHTTPException)
def custom_http_exception_handler(request: Request, exc: HTTPException):
    try:
        if exc.status_code == 401:
            print(request.__dict__)
            return error_templates.TemplateResponse(
                "401.html",
                {
                    "request": (exc.burning_request if hasattr(exc, "burning_request") else request),
                    "current_url": request.url,
                    "current_method": request.method,
                    "alert": Alert("Вы не обладаете достаточными правами для просмотра этой страницы!"
                                   "Возможно, вам надо авторизоваться...", Alert.ERROR)
                },
                status_code=401,
            )

        elif exc.status_code == 404:
            return error_templates.TemplateResponse("404.html", {
                "request": (exc.burning_request if hasattr(exc, "burning_request") else request),
                "detail": exc.detail,
                "alert": Alert("Похоже данной страницы не существует...", Alert.ERROR)})
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": f"Oops! did something. There goes a rainbow..."},
        )
    except FileExistsError as e:
        print("произошла ошибка в функции обработки ошибок:", e)
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": f"Oops! did something. There goes a rainbow..."},
        )


if __name__ == "__main__":
    try:
        create_pages()
    except TransactionIntegrityError:
        pass
    with db_session:
        show(m.Human.select().show())
        # m.Admin(
        #     username="Kalekdfi34nsDdanijjil55",
        #     hash_password="KalekinDaniijjl123",
        #     name="Даниил",
        #     surname="Калекин",
        #     email="Kalek4sdf3injjDa5d5niil123@mail.ru",
        # )
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
