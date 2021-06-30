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
from app.public_routers.security import public_security
from app.utils.utils_of_security import security
from app.utils.basic_utils import async_iterator_wrapper as aiwrap
from app.utils.html_utils import Alert
from app.db.create_db_content import create_pages
from app.db_router.routers import db_route
from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.db import models as m
from app.utils.jinja2_utils import public_templates
from app.utils.exceptions import ChildHTTPException as HTTPException
from app.pydantic_models.response_models import GenResp, Ajax200Answer
from app.utils.responses import RedirectResponseWithBody
from app.pydantic_models.response_models import Ajax300Answer
from app.pydantic_models.gen import output_ent as out_pd

app = FastAPI(
    tags=["public"],
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

app.mount("/public", StaticFiles(directory="app/content/public"), name="public")
app.mount("/static", StaticFiles(directory="app/content/static"), name="static")
app.mount("/scripts", StaticFiles(directory="app/content/scripts"), name="scripts")
app.mount("/stiles", StaticFiles(directory="app/content/stiles"), name="stiles")
app.mount("/fonts", StaticFiles(directory="app/content/fonts"), name="fonts")
app.mount("/docs", StaticFiles(directory="app/content/public/docs"), name="docs")
app.mount("/img", StaticFiles(directory="app/content/public/images"), name="img")

app.include_router(public_router)
app.include_router(user)
app.include_router(smm)
app.include_router(direction_expert)
app.include_router(admin)
app.include_router(dev)
app.include_router(db_route)

app.include_router(public_security)
app.include_router(security_user)
app.include_router(security_smmer)
app.include_router(security_direction_expert)
app.include_router(security_admin)
app.include_router(security_dev)

app.include_router(security)


@app.get("/test", response_class=HTMLResponse)
async def root():
    return FileResponse("index.html")


@app.get("/test_new_sys")
def test_new_sys(request: Request):
    return GenResp(Ajax200Answer, request, ".html", public_templates, {}, alert=Alert, shell={})


@app.exception_handler(StarletteHTTPException)
def custom_http_exception_handler(request: Request, exc: HTTPException):
    try:
        if exc.status_code == 401:
            print(request.__dict__)
            if hasattr(exc, "burning_request") and hasattr(exc.burning_request, "__dict__"):
                request.__dict__.update(exc.burning_request.__dict__)
            return error_templates.TemplateResponse(
                "401.html",
                {
                    "request": request,
                    "current_url": request.url,
                    "current_method": request.method,
                    "alert": Alert(
                        "Вы не обладаете достаточными правами для просмотра этой страницы!"
                        "Возможно, вам надо авторизоваться...",
                        Alert.ERROR,
                    ),
                },
                status_code=401,
            )
        elif exc.status_code == 403:
            print(request.__dict__)
            if hasattr(exc, "burning_request") and hasattr(exc.burning_request, "__dict__"):
                request.__dict__.update(exc.burning_request.__dict__)
            return error_templates.TemplateRedirectResponse(
                "/log_in",
                "403.html",
                {
                    "url": "/log_in",
                    "request": request,
                    "alert": Alert("Вам необходимо авторизоваться, чтобы просматривать эту страницу", Alert.ERROR),
                },
            )
            # return  RedirectResponseWithBody(f"/log_in", Ajax300Answer(
            #     url=f"/log_in",
            #     alert=Alert("Вам необходимо авторизоваться, чтобы просматривать эту страницу", Alert.ERROR),
            #     request=request))
        elif exc.status_code == 404:
            print(request.__dict__)
            if hasattr(exc, "burning_request") and hasattr(exc.burning_request, "__dict__"):
                request.__dict__.update(exc.burning_request.__dict__)
            return error_templates.TemplateResponse(
                "404.html",
                {
                    "request": (exc.burning_request if hasattr(exc, "burning_request") else request),
                    "detail": exc.detail,
                    "alert": Alert("Похоже данной страницы не существует...", Alert.ERROR),
                },
            )
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
    # from typing import ForwardRef
    # print([i.__forward_arg__ for i in out_pd.Admin.__fields__['questions'].type_.__dict__['__args__'] if type(i) == ForwardRef])
    # # import typing

    # typing._UnionGenericAlias
    # list.__class_getitem__(*(1,))
    # print(a[(2,)])
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
