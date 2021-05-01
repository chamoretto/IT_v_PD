# -*- coding: utf-8 -*-

"""Главный файл нашего web-приложения"""

from fastapi import FastAPI
import uvicorn


from fastapi import Depends, FastAPI

from .dependencies import *
from .public_routers.routers import public_router
from .users.routers import user
from .smmers.routers import smm
from .admins.routers import admin
from .developers.routers import dev

app = FastAPI()


app.include_router(public_router)
app.include_router(user)
app.include_router(smm)
app.include_router(admin)
app.include_router(dev)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
