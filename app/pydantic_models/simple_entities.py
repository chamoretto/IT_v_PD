from enum import Enum
from typing import Any

from app.pydantic_models.standart_methhods_redefinition import BaseModel


class Partner(BaseModel):
    id: int
    name: str
    image: str


class Socials(BaseModel):
    id: int
    name: str
    icon: str
    link: str
