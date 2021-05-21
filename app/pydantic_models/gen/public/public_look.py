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
from app.pydantic_models.gen.output_ent import Task
from app.pydantic_models.gen.output_ent import MarkWork
from app.pydantic_models.gen.output_ent import DirectionExpert
from app.pydantic_models.gen.output_ent import SimpleEntity
from app.pydantic_models.gen.output_ent import Smm
from app.pydantic_models.gen.output_ent import HumanContacts
from app.pydantic_models.gen.output_ent import CompetitionDirection
from app.pydantic_models.gen.output_ent import Admin
from app.pydantic_models.gen.output_ent import Human
from app.pydantic_models.gen.output_ent import User
from app.pydantic_models.gen.output_ent import News
from app.pydantic_models.gen.output_ent import Direction
from app.pydantic_models.gen.output_ent import Criterion
from app.pydantic_models.gen.output_ent import Page
from app.pydantic_models.gen.output_ent import Competition
from app.pydantic_models.gen.output_ent import Developer
from app.pydantic_models.gen.output_ent import UserWork
from app.settings.config import HOME_DIR


Question = ForwardRef("Question")



class Question(BaseModel):
	question_title: Optional[str] = ''
	question: str
	pages: Set[Union[int, Page]] = []
	answer_email: Optional[str] = ''
	human: Union[int, Human, None] = None
	was_read: bool = False
	was_answered: bool = False

	class Config:
		orm_mode = True


Question.update_forward_refs()


if __name__ == '__main__':
	from os import chdir

	chdir(HOME_DIR)