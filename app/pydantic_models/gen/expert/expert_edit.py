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
from app.pydantic_models.gen.output_ent import CompetitionDirection
from app.pydantic_models.gen.output_ent import Page
from app.pydantic_models.gen.output_ent import User
from app.pydantic_models.gen.output_ent import SimpleEntity
from app.pydantic_models.gen.output_ent import HumanContacts
from app.pydantic_models.gen.output_ent import Smm
from app.pydantic_models.gen.output_ent import Admin
from app.pydantic_models.gen.output_ent import Direction
from app.pydantic_models.gen.output_ent import Human
from app.pydantic_models.gen.output_ent import Question
from app.pydantic_models.gen.output_ent import News
from app.pydantic_models.gen.output_ent import Competition
from app.pydantic_models.gen.output_ent import Developer
from app.settings.config import HOME_DIR


DirectionExpert = ForwardRef("DirectionExpert")
Task = ForwardRef("Task")
UserWork = ForwardRef("UserWork")
Criterion = ForwardRef("Criterion")
MarkWork = ForwardRef("MarkWork")


class DirectionExpert(BaseModel):
    id: int
    username: str
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


class Task(BaseModel):
    competition_direction: Union[Tuple[str, int], CompetitionDirection]
    task_document: Optional[str] = ""
    description: Optional[str] = ""
    start: datetime
    end: datetime

    @validator("start", pre=True, always=True)
    def start_to_datetime_validator(cls, value):
        return PydanticValidators.datetime(cls, value)

    @validator("end", pre=True, always=True)
    def end_to_datetime_validator(cls, value):
        return PydanticValidators.datetime(cls, value)

    class Config:
        orm_mode = True


class UserWork(BaseModel):
    mark_works: Set[Union[Tuple[int, int, int], MarkWork]] = []
    upload_date: datetime

    @validator("upload_date", pre=True, always=True)
    def upload_date_to_datetime_validator(cls, value):
        return PydanticValidators.datetime(cls, value)

    class Config:
        orm_mode = True


class Criterion(BaseModel):
    task: Union[int, Task]
    name: str
    description: Optional[str] = ""
    max_value: Optional[float] = None

    class Config:
        orm_mode = True


class MarkWork(BaseModel):
    criterion: Union[int, Criterion]
    user_work: Union[Tuple[int, int], UserWork]
    value: int

    class Config:
        orm_mode = True


DirectionExpert.update_forward_refs()
Task.update_forward_refs()
UserWork.update_forward_refs()
Criterion.update_forward_refs()
MarkWork.update_forward_refs()


if __name__ == "__main__":
    from os import chdir

    chdir(HOME_DIR)
