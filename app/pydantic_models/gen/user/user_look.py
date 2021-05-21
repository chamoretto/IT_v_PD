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
from app.pydantic_models.gen.output_ent import News
from app.pydantic_models.gen.output_ent import Direction
from app.pydantic_models.gen.output_ent import Criterion
from app.pydantic_models.gen.output_ent import Page
from app.pydantic_models.gen.output_ent import Competition
from app.pydantic_models.gen.output_ent import Question
from app.pydantic_models.gen.output_ent import Developer
from app.settings.config import HOME_DIR


User = ForwardRef("User")
UserWork = ForwardRef("UserWork")



class User(BaseModel):
	id: int
	username: str
	name: str
	surname: str
	email: str
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict, list]] = {}
	questions: Set[Union[int, Question]] = []
	date_of_birth: date
	about_program: Optional[str] = None
	direction: Optional[str] = None

	class Config:
		orm_mode = True


class UserWork(BaseModel):
	task: Union[int, Task]
	work: Optional[str] = ''
	mark_works: Set[Union[Tuple[int, int, int], MarkWork]] = []
	user: Union[int, User]
	upload_date: datetime


	@validator("upload_date", pre=True, always=True)
	def upload_date_to_datetime_validator(cls, value):
		return PydanticValidators.datetime(cls, value)

	class Config:
		orm_mode = True


User.update_forward_refs()
UserWork.update_forward_refs()


if __name__ == '__main__':
	from os import chdir

	chdir(HOME_DIR)