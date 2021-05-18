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

PkHuman = Union[int, Human]
PkAdmin = Union[int, Admin]
PkUser = Union[int, User]
PkSmm = Union[int, Smm]
PkDeveloper = Union[int, Developer]
PkHumanContacts = Union[int, HumanContacts]
PkDirectionExpert = Union[int, DirectionExpert]
PkCompetition = Union[int, Competition]
PkDirection = Union[str, Direction]
PkCompetitionDirection = Union[Tuple[str, int], CompetitionDirection]
PkTask = Union[int, Task]
PkUserWork = Union[Tuple[int, int], UserWork]
PkCriterion = Union[int, Criterion]
PkMarkWork = Union[Tuple[int, int, int], MarkWork]
PkPage = Union[int, Page]
PkQuestion = Union[int, Question]
PkSimpleEntity = Union[str, SimpleEntity]
PkNews = Union[int, News]

OptionalPkHuman = Union[int, Human, None]
OptionalPkAdmin = Union[int, Admin, None]
OptionalPkUser = Union[int, User, None]
OptionalPkSmm = Union[int, Smm, None]
OptionalPkDeveloper = Union[int, Developer, None]
OptionalPkHumanContacts = Union[int, HumanContacts, None]
OptionalPkDirectionExpert = Union[int, DirectionExpert, None]
OptionalPkCompetition = Union[int, Competition, None]
OptionalPkDirection = Union[str, Direction, None]
OptionalPkCompetitionDirection = Union[Tuple[str, int], CompetitionDirection, None]
OptionalPkTask = Union[int, Task, None]
OptionalPkUserWork = Union[Tuple[int, int], UserWork, None]
OptionalPkCriterion = Union[int, Criterion, None]
OptionalPkMarkWork = Union[Tuple[int, int, int], MarkWork, None]
OptionalPkPage = Union[int, Page, None]
OptionalPkQuestion = Union[int, Question, None]
OptionalPkSimpleEntity = Union[str, SimpleEntity, None]
OptionalPkNews = Union[int, News, None]

SetPkHuman = Set[Union[int, Human]]
SetPkAdmin = Set[Union[int, Admin]]
SetPkUser = Set[Union[int, User]]
SetPkSmm = Set[Union[int, Smm]]
SetPkDeveloper = Set[Union[int, Developer]]
SetPkHumanContacts = Set[Union[int, HumanContacts]]
SetPkDirectionExpert = Set[Union[int, DirectionExpert]]
SetPkCompetition = Set[Union[int, Competition]]
SetPkDirection = Set[Union[str, Direction]]
SetPkCompetitionDirection = Set[Union[Tuple[str, int], CompetitionDirection]]
SetPkTask = Set[Union[int, Task]]
SetPkUserWork = Set[Union[Tuple[int, int], UserWork]]
SetPkCriterion = Set[Union[int, Criterion]]
SetPkMarkWork = Set[Union[Tuple[int, int, int], MarkWork]]
SetPkPage = Set[Union[int, Page]]
SetPkQuestion = Set[Union[int, Question]]
SetPkSimpleEntity = Set[Union[str, SimpleEntity]]
SetPkNews = Set[Union[int, News]]


class Human(BaseModel):
	id: Optional[int] = None
	username: Optional[str] = None
	password: Optional[None] = None
	name: Optional[str] = None
	surname: Optional[str] = None
	email: Optional[str] = None
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []

	class Config:
		orm_mode = True


class Admin(BaseModel):
	id: Optional[int] = None
	username: Optional[str] = None
	password: Optional[None] = None
	name: Optional[str] = None
	surname: Optional[str] = None
	email: Optional[str] = None
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []

	class Config:
		orm_mode = True


class User(BaseModel):
	id: Optional[int] = None
	username: Optional[str] = None
	password: Optional[None] = None
	name: Optional[str] = None
	surname: Optional[str] = None
	email: Optional[str] = None
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []
	date_of_birth: Optional[date] = None
	about_program: Optional[str] = None
	direction: Optional[str] = None
	visible_about_program_field: Optional[bool] = False

	class Config:
		orm_mode = True


class Smm(BaseModel):
	id: Optional[int] = None
	username: Optional[str] = None
	password: Optional[None] = None
	name: Optional[str] = None
	surname: Optional[str] = None
	email: Optional[str] = None
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []

	class Config:
		orm_mode = True


class Developer(BaseModel):
	id: Optional[int] = None
	username: Optional[str] = None
	password: Optional[None] = None
	name: Optional[str] = None
	surname: Optional[str] = None
	email: Optional[str] = None
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []

	class Config:
		orm_mode = True


class HumanContacts(BaseModel):
	phone: Optional[str] = ''
	vk: Optional[str] = ''
	insagramm: Optional[str] = ''
	facebook: Optional[str] = ''
	telegram: Optional[str] = ''
	home_adress: Optional[str] = ''

	class Config:
		orm_mode = True


class DirectionExpert(BaseModel):
	id: Optional[int] = None
	username: Optional[str] = None
	password: Optional[None] = None
	name: Optional[str] = None
	surname: Optional[str] = None
	email: Optional[str] = None
	human_contacts: Union[int, HumanContacts, None] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Union[Json, dict]] = {}
	questions: Set[Union[int, Question]] = []

	class Config:
		orm_mode = True


class Competition(BaseModel):
	id: Optional[int] = None
	name: Optional[str] = None
	start: Optional[datetime] = None
	end: Optional[datetime] = None
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
	name: Optional[str] = None
	icon: Optional[str] = None
	video_lessons: Optional[Union[Json, dict]] = {}

	class Config:
		orm_mode = True


class CompetitionDirection(BaseModel):
	directions: Union[str, Direction, None] = None
	questions: Optional[None] = None
	competition: Union[int, Competition, None] = None
	direction_experts: Set[Union[int, DirectionExpert]] = []

	class Config:
		orm_mode = True


class Task(BaseModel):
	id: Optional[int] = None
	competition_direction: Union[Tuple[str, int], CompetitionDirection, None] = None
	task_document: Optional[str] = ''
	description: Optional[str] = ''
	start: Optional[datetime] = None
	end: Optional[datetime] = None


	@validator("start", pre=True, always=True)
	def start_to_datetime_validator(cls, value):
		return PydanticValidators.datetime(cls, value)


	@validator("end", pre=True, always=True)
	def end_to_datetime_validator(cls, value):
		return PydanticValidators.datetime(cls, value)

	class Config:
		orm_mode = True


class UserWork(BaseModel):
	task: Union[int, Task, None] = None
	work: Optional[str] = ''
	mark_works: Set[Union[Tuple[int, int, int], MarkWork]] = []
	user: Union[int, User, None] = None
	upload_date: Optional[datetime] = None


	@validator("upload_date", pre=True, always=True)
	def upload_date_to_datetime_validator(cls, value):
		return PydanticValidators.datetime(cls, value)

	class Config:
		orm_mode = True


class Criterion(BaseModel):
	id: Optional[int] = None
	task: Union[int, Task, None] = None
	name: Optional[str] = None
	description: Optional[str] = ''
	max_value: Optional[float] = None
	mark_works: Set[Union[Tuple[int, int, int], MarkWork]] = []

	class Config:
		orm_mode = True


class MarkWork(BaseModel):
	criterion: Union[int, Criterion, None] = None
	user_work: Union[Tuple[int, int], UserWork, None] = None
	value: Optional[int] = None

	class Config:
		orm_mode = True


class Page(BaseModel):
	id: Optional[int] = None
	page_url: Optional[str] = ''
	page_path: Optional[str] = ''
	is_header: Optional[bool] = False
	visible: Optional[bool] = False
	root_page: Union[int, Page, None] = None
	child_pages: Set[Union[int, Page]] = []
	title: Optional[str] = ''
	questions: Set[Union[int, Question]] = []

	class Config:
		orm_mode = True


class Question(BaseModel):
	id: Optional[int] = None
	question_title: Optional[str] = ''
	question: Optional[str] = None
	answer: Optional[str] = ''
	pages: Set[Union[int, Page]] = []
	answer_email: Optional[str] = ''
	human: Union[int, Human, None] = None
	was_read: Optional[bool] = False
	was_answered: Optional[bool] = False

	class Config:
		orm_mode = True


class SimpleEntity(BaseModel):
	key: Optional[str] = None
	data: Optional[Union[Json, dict]] = {}

	class Config:
		orm_mode = True


class News(BaseModel):
	id: Optional[int] = None
	page_url: Optional[str] = ''
	page_path: Optional[str] = ''
	is_header: Optional[bool] = False
	visible: Optional[bool] = False
	root_page: Union[int, Page, None] = None
	child_pages: Set[Union[int, Page]] = []
	title: Optional[str] = ''
	questions: Set[Union[int, Question]] = []
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


if __name__ == '__main__':
	from os import chdir

	chdir(HOME_DIR)
