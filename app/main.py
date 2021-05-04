# -*- coding: utf-8 -*-

"""Главный файл нашего web-приложения"""

from fastapi import FastAPI
import uvicorn
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse


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
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


from app.utils.utils_of_security import security

from app.db.db_utils import connect_with_db
from app.db.db_utils import db_session
from app.db.raw_models import Admin
from app.pydantic_models.standart_methhods_redefinition import BaseModel


app = FastAPI()

app.mount("/public", StaticFiles(directory="content/public"), name="public")
app.mount("/static", StaticFiles(directory="content/static"), name="static")
app.mount("/_scripts", StaticFiles(directory="content/scripts"), name="_scripts")
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
async def getimg(some_func: str =""):
    try:
        some_func: str = trololo
        return some_func()
    except Exception:
        return { '1' : 1}


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    print(request)
    print(request)
    print([exc])
    if exc.status_code == 404:
        return error_templates.TemplateResponse("404.html", {"request": request})
    # return RedirectResponse("/")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"Oops! did something. There goes a rainbow..."},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
