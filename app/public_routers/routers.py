from os.path import join as os_join

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel


public_router = APIRouter()


@public_router.get('/')
async def start_public_router():
    return {1: 1}


# @public_router.get('/content/public/{file_path:path}')
# async def get_public_files(file_path: str):
#     file_path = os_join("content", "public", file_path)
#     return FileResponse(file_path)

public_router.mount("/public", StaticFiles(directory="content/public"), name="public")
public_router.mount("/static", StaticFiles(directory="content/static"), name="static")
public_router.mount("/scripts", StaticFiles(directory="content/scripts"), name="scripts")
public_router.mount("/stiles", StaticFiles(directory="content/stiles"), name="stiles")
public_router.mount("/fonts", StaticFiles(directory="content/fonts"), name="fonts")
public_router.mount("/docs", StaticFiles(directory="content/public/docs"), name="docs")
public_router.mount("/img", StaticFiles(directory="content/public/images"), name="img")
