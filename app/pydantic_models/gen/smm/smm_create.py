# -*- coding: utf-8 -*-


""" Этот код генерируется автоматически,
функцией create_pd_models файла app/db/create_pydantic_models.py
-------!!!!!! Ни одно изменение не сохранится в этом файле. !!!!!-----

Тут объявляются pydantic-модели, в которых присутствуют все сущности БД
и все атрибуты сущностей"""

from typing import Set, Union, List, Dict, Tuple, ForwardRef
from typing import Optional, Literal, Any
from pydantic import Json, root_validator, validator
from datetime import date, datetime, time

from app.pydantic_models.standart_methhods_redefinition import BaseModel, as_form
from app.pydantic_models.standart_methhods_redefinition import PydanticValidators
from app.pydantic_models.gen.input_ent import DirectionExpert
from app.pydantic_models.gen.input_ent import Criterion
from app.pydantic_models.gen.input_ent import Admin
from app.pydantic_models.gen.input_ent import Question
from app.pydantic_models.gen.input_ent import Competition
from app.pydantic_models.gen.input_ent import CompetitionDirection
from app.pydantic_models.gen.input_ent import UserWork
from app.pydantic_models.gen.input_ent import User
from app.pydantic_models.gen.input_ent import SimpleEntity
from app.pydantic_models.gen.input_ent import HumanContacts
from app.pydantic_models.gen.input_ent import Task
from app.pydantic_models.gen.input_ent import MarkWork
from app.pydantic_models.gen.input_ent import Direction
from app.pydantic_models.gen.input_ent import Human
from app.pydantic_models.gen.input_ent import Developer
from app.settings.config import HOME_DIR


Smm = ForwardRef("Smm")
Page = ForwardRef("Page")
News = ForwardRef("News")


class Smm(BaseModel):
    username: str
    password: Optional[str] = None
    name: str
    surname: str
    email: str
    human_contacts: Union[int, HumanContacts, None] = None
    photo: Optional[str] = ""
    status: Optional[str] = ""
    description: Optional[str] = ""
    scopes: Optional[Union[Json, dict, list]] = []
    questions: Set[Union[int, Question]] = []

    class Config:
        orm_mode = True


class Page(BaseModel):
    page_url: Optional[str] = ""
    page_path: Optional[str] = ""
    visible: bool = False
    root_page: Union[int, Page, None] = None
    title: Optional[str] = ""
    questions: Set[Union[int, Question]] = []
    page_type: Optional[str] = ""

    class Config:
        orm_mode = True


class News(BaseModel):
    page_url: Optional[str] = ""
    page_path: Optional[str] = ""
    visible: bool = False
    root_page: Union[int, Page, None] = None
    title: Optional[str] = ""
    questions: Set[Union[int, Question]] = []
    page_type: Optional[str] = ""
    auto_publish: Optional[datetime] = None
    image: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None

    @validator("auto_publish", pre=True, always=True)
    def auto_publish_to_datetime_validator(cls, value):
        return PydanticValidators.datetime(cls, value)

    class Config:
        orm_mode = True


Smm.update_forward_refs()
Page.update_forward_refs()
News.update_forward_refs()


if __name__ == "__main__":
    from os import chdir

    chdir(HOME_DIR)
