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
from app.pydantic_models.gen.input_ent import HumanContacts
from app.settings.config import HOME_DIR


Human = ForwardRef("Human")
Admin = ForwardRef("Admin")
User = ForwardRef("User")
Smm = ForwardRef("Smm")
Developer = ForwardRef("Developer")
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
	username: str
	password: Optional[None] = None
	name: str
	surname: str
	email: str
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}

	class Config:
		orm_mode = True


class Admin(BaseModel):
	username: str
	password: Optional[None] = None
	name: str
	surname: str
	email: str
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []

	class Config:
		orm_mode = True


class User(BaseModel):
	username: str
	password: Optional[None] = None
	name: str
	surname: str
	email: str
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []
	date_of_birth: date
	about_program: Optional[str] = None
	direction: Optional[str] = None
	visible_about_program_field: bool = False

	class Config:
		orm_mode = True


class Smm(BaseModel):
	username: str
	password: Optional[None] = None
	name: str
	surname: str
	email: str
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []

	class Config:
		orm_mode = True


class Developer(BaseModel):
	password: Optional[None] = None

	class Config:
		orm_mode = True


class DirectionExpert(BaseModel):
	username: str
	password: Optional[None] = None
	name: str
	surname: str
	email: str
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []

	class Config:
		orm_mode = True


class Competition(BaseModel):
	id: int
	name: str
	start: datetime
	end: datetime
	description: Optional[str] = ''
	document: Optional[str] = ''


	@validator("start", pre=True, always=True)
	def start_to_datetime_validator(cls, value):
		return PydanticValidators.datetime(cls, value)


	@validator("end", pre=True, always=True)
	def end_to_datetime_validator(cls, value):
		return PydanticValidators.datetime(cls, value)

	class Config:
		orm_mode = True


class Direction(BaseModel):
	name: str
	icon: str
	video_lessons: Optional[Union[Json, dict]] = {}

	class Config:
		orm_mode = True


class CompetitionDirection(BaseModel):
	questions: Optional[None] = None

	class Config:
		orm_mode = True


class Task(BaseModel):
	competition_direction: Union[Tuple[str, int], CompetitionDirection]
	task_document: Optional[str] = ''
	description: Optional[str] = ''
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
	task: Union[int, Task]
	work: Optional[str] = ''
	mark_works: Set[Union[Tuple[int, int, int], MarkWork]] = []

	class Config:
		orm_mode = True


class Criterion(BaseModel):
	task: Union[int, Task]
	name: str
	description: Optional[str] = ''
	max_value: Optional[float] = None

	class Config:
		orm_mode = True


class MarkWork(BaseModel):
	criterion: Union[int, Criterion]
	user_work: Union[Tuple[int, int], UserWork]
	value: int

	class Config:
		orm_mode = True


class Page(BaseModel):
	page_url: Optional[str] = ''
	page_path: Optional[str] = ''
	is_header: bool = False
	visible: bool = False
	root_page: Union[int, Page, None] = None
	title: Optional[str] = ''
	questions: Set[Union[int, Question]] = []
	page_type: Optional[str] = ''

	class Config:
		orm_mode = True


class Question(BaseModel):
	question_title: Optional[str] = ''
	question: str
	pages: Set[Union[int, Page]] = []
	answer_email: Optional[str] = ''
	was_read: bool = False
	was_answered: bool = False

	class Config:
		orm_mode = True


class SimpleEntity(BaseModel):
	key: str
	data: Optional[Union[Json, dict]] = {}

	class Config:
		orm_mode = True


class News(BaseModel):
	page_url: Optional[str] = ''
	page_path: Optional[str] = ''
	is_header: bool = False
	visible: bool = False
	root_page: Union[int, Page, None] = None
	title: Optional[str] = ''
	questions: Set[Union[int, Question]] = []
	page_type: Optional[str] = ''
	auto_publish: Optional[datetime] = None
	image: Optional[str] = None
	author: Optional[str] = None
	description: Optional[str] = None


	@validator("auto_publish", pre=True, always=True)
	def auto_publish_to_datetime_validator(cls, value):
		return PydanticValidators.datetime(cls, value)

	class Config:
		orm_mode = True


Human.update_forward_refs()
Admin.update_forward_refs()
User.update_forward_refs()
Smm.update_forward_refs()
Developer.update_forward_refs()
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


if __name__ == '__main__':
	from os import chdir

	chdir(HOME_DIR)