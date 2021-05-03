# -*- coding: utf-8 -*-

"""Главный файл нашего web-приложения"""

from fastapi import FastAPI
import uvicorn
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from fastapi import Depends, FastAPI

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
from app.admins.security import admin as security_admin, admin_oauth2_scheme
from app.developers.security import dev as security_dev
from app.db.db_utils import connect_with_db
from app.db.db_utils import db_session
from app.db.raw_models import Admin
from app.pydantic_models.standart_methhods_redefinition import BaseModel


app = FastAPI()


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


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/test", response_class=HTMLResponse)
async def root():
    return FileResponse('index.html')


@app.get('/gimg')
async def getimg():
    return { '1' : 1}


if __name__ == "__main__":
    print(admin_oauth2_scheme.tokenUrl)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
