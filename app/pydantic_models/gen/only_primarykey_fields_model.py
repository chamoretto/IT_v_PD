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
from app.settings.config import HOME_DIR


Human = ForwardRef("Human")
Admin = ForwardRef("Admin")
User = ForwardRef("User")
Smm = ForwardRef("Smm")
Developer = ForwardRef("Developer")
HumanContacts = ForwardRef("HumanContacts")
DirectionExpert = ForwardRef("DirectionExpert")
Competition = ForwardRef("Competition")
Direction = ForwardRef("Direction")
CompetitionDirection = ForwardRef("CompetitionDirection")
Task = ForwardRef("Task")
UserWork = ForwardRef("UserWork")
Criterion = ForwardRef("Criterion")
MarkWork = ForwardRef("MarkWork")
Page = ForwardRef("Page")
Question = ForwardRef("Question")
SimpleEntity = ForwardRef("SimpleEntity")
News = ForwardRef("News")


class Human(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Admin(BaseModel):
    id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Smm(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Developer(BaseModel):
    id: int

    class Config:
        orm_mode = True


class HumanContacts(BaseModel):
    human: Union[int, Human]

    class Config:
        orm_mode = True


class DirectionExpert(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Competition(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Direction(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CompetitionDirection(BaseModel):
    class Config:
        orm_mode = True


class Task(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserWork(BaseModel):
    class Config:
        orm_mode = True


class Criterion(BaseModel):
    id: int

    class Config:
        orm_mode = True


class MarkWork(BaseModel):
    class Config:
        orm_mode = True


class Page(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Question(BaseModel):
    id: int

    class Config:
        orm_mode = True


class SimpleEntity(BaseModel):
    key: str

    class Config:
        orm_mode = True


class News(BaseModel):
    id: int

    class Config:
        orm_mode = True


Human.update_forward_refs()
Admin.update_forward_refs()
User.update_forward_refs()
Smm.update_forward_refs()
Developer.update_forward_refs()
HumanContacts.update_forward_refs()
DirectionExpert.update_forward_refs()
Competition.update_forward_refs()
Direction.update_forward_refs()
CompetitionDirection.update_forward_refs()
Task.update_forward_refs()
UserWork.update_forward_refs()
Criterion.update_forward_refs()
MarkWork.update_forward_refs()
Page.update_forward_refs()
Question.update_forward_refs()
SimpleEntity.update_forward_refs()
News.update_forward_refs()


if __name__ == "__main__":
    from os import chdir

    chdir(HOME_DIR)
