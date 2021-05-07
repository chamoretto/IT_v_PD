# -*- coding: utf-8 -*-


""" Этот код генерируется автоматически,
функцией create_pd_models файла app/db/create_pydantic_models.py
-------!!!!!! Ни одно изменение не сохранится в этом файле. !!!!!-----

Тут объявляются pydantic-модели, в которых присутствуют все сущности БД
и все атрибуты сущностей"""

from typing import Set, Union, List, Dict, Tuple, ForwardRef
from typing import Optional, Literal, Any
from pydantic import Json
from datetime import date, datetime, time

from app.pydantic_models.standart_methhods_redefinition import BaseModel
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
PkCompetition = Union[str, Competition]
PkDirection = Union[str, Direction]
PkCompetitionDirection = Union[Tuple[str, str], CompetitionDirection]
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
OptionalPkCompetition = Union[str, Competition, None]
OptionalPkDirection = Union[str, Direction, None]
OptionalPkCompetitionDirection = Union[Tuple[str, str], CompetitionDirection, None]
OptionalPkTask = Union[int, Task, None]
OptionalPkUserWork = Union[Tuple[int, int], UserWork, None]
OptionalPkCriterion = Union[int, Criterion, None]
OptionalPkMarkWork = Union[Tuple[int, int, int], MarkWork, None]
OptionalPkPage = Union[int, Page, None]
OptionalPkQuestion = Union[int, Question, None]
OptionalPkSimpleEntity = Union[str, SimpleEntity, None]
OptionalPkNews = Union[int, News, None]


class Human(BaseModel):
	id: int
	username: str
	hash_password: str
	name: str
	surname: str
	email: str
	human_contacts: Optional[OptionalPkHumanContacts] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Json] = {}
	questions: Set[PkQuestion] = []

	class Config:
		orm_mode = True


class Admin(BaseModel):
	id: int
	username: str
	hash_password: str
	name: str
	surname: str
	email: str
	human_contacts: Optional[OptionalPkHumanContacts] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Json] = {}
	questions: Set[PkQuestion] = []

	class Config:
		orm_mode = True


class User(BaseModel):
	id: int
	username: str
	hash_password: str
	name: str
	surname: str
	email: str
	human_contacts: Optional[OptionalPkHumanContacts] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Json] = {}
	questions: Set[PkQuestion] = []
	date_of_birth: date
	user_works: Set[PkUserWork] = []
	about_program: Optional[str] = None
	direction: Optional[str] = None
	visible_about_program_field: bool = False

	class Config:
		orm_mode = True


class Smm(BaseModel):
	id: int
	username: str
	hash_password: str
	name: str
	surname: str
	email: str
	human_contacts: Optional[OptionalPkHumanContacts] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Json] = {}
	questions: Set[PkQuestion] = []

	class Config:
		orm_mode = True


class Developer(BaseModel):
	id: int
	username: str
	hash_password: str
	name: str
	surname: str
	email: str
	human_contacts: Optional[OptionalPkHumanContacts] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Json] = {}
	questions: Set[PkQuestion] = []

	class Config:
		orm_mode = True


class HumanContacts(BaseModel):
	human: PkHuman
	phone: Optional[str] = ''
	vk: Optional[str] = ''
	insagramm: Optional[str] = ''
	facebook: Optional[str] = ''
	home_adress: Optional[str] = ''
	telegram: Optional[str] = ''

	class Config:
		orm_mode = True


class DirectionExpert(BaseModel):
	id: int
	username: str
	hash_password: str
	name: str
	surname: str
	email: str
	human_contacts: Optional[OptionalPkHumanContacts] = None
	photo: Optional[str] = ''
	status: Optional[str] = ''
	description: Optional[str] = ''
	scopes: Optional[Json] = {}
	questions: Set[PkQuestion] = []
	competition_directions: Set[PkCompetitionDirection] = []

	class Config:
		orm_mode = True


class Competition(BaseModel):
	name: str
	start: datetime
	end: datetime
	description: Optional[str] = ''
	competition_direction: Set[PkCompetitionDirection] = []
	document: Optional[str] = ''

	class Config:
		orm_mode = True


class Direction(BaseModel):
	name: str
	icon: str
	competition_direction: Set[PkCompetitionDirection] = []
	video_lessons: Optional[Json] = {}

	class Config:
		orm_mode = True


class CompetitionDirection(BaseModel):
	directions: PkDirection
	competition: PkCompetition
	tasks: Set[PkTask] = []
	direction_experts: Set[PkDirectionExpert] = []
	criterions: Set[PkCriterion] = []

	class Config:
		orm_mode = True


class Task(BaseModel):
	id: int
	competition_direction: PkCompetitionDirection
	task_document: Optional[str] = ''
	description: Optional[str] = ''
	start: datetime
	end: datetime
	user_works: Set[PkUserWork] = []

	class Config:
		orm_mode = True


class UserWork(BaseModel):
	mark_works: Set[PkMarkWork] = []
	user: PkUser
	task: PkTask
	work: Optional[str] = ''
	upload_date: datetime
	mark: Optional[str] = ''

	class Config:
		orm_mode = True


class Criterion(BaseModel):
	id: int
	competition_direction: PkCompetitionDirection
	name: str
	description: Optional[str] = ''
	max_value: Optional[float] = None
	mark_works: Set[PkMarkWork] = []

	class Config:
		orm_mode = True


class MarkWork(BaseModel):
	criterion: PkCriterion
	user_work: PkUserWork
	value: int

	class Config:
		orm_mode = True


class Page(BaseModel):
	id: int
	page_url: Optional[str] = ''
	page_path: Optional[str] = ''
	is_header: bool = False
	visible: bool = False
	child_pages: Set[PkPage] = []
	root_page: Optional[OptionalPkPage] = None
	title: Optional[str] = ''
	questions: Set[PkQuestion] = []

	class Config:
		orm_mode = True


class Question(BaseModel):
	id: int
	question_title: Optional[str] = ''
	question: str
	answer: Optional[str] = ''
	pages: Set[PkPage] = []
	answer_email: Optional[str] = ''
	human: Optional[OptionalPkHuman] = None
	was_read: bool = False
	was_answered: bool = False

	class Config:
		orm_mode = True


class SimpleEntity(BaseModel):
	key: str
	data: Optional[Json] = {}

	class Config:
		orm_mode = True


class News(BaseModel):
	id: int
	page_url: Optional[str] = ''
	page_path: Optional[str] = ''
	is_header: bool = False
	visible: bool = False
	child_pages: Set[PkPage] = []
	root_page: Optional[OptionalPkPage] = None
	title: Optional[str] = ''
	questions: Set[PkQuestion] = []
	auto_publish: Optional[datetime] = None
	image: Optional[str] = None
	author: Optional[str] = None
	description: Optional[str] = None

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
