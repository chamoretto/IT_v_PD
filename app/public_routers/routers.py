from os.path import join as os_join

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.dependencies import *

from app.pydantic_models.standart_methhods_redefinition import BaseModel


public_router = APIRouter()


@public_router.get('/')
async def start_public_router():
    return {1: 1}


@public_router.get('/content/public/{file_path:path}')
async def get_public_files(file_path: str):
    file_path = os_join("content", "public", file_path)
    return FileResponse(file_path)
