from datetime import date
from datetime import datetime
from pony.orm import *

db = Database()


class Human(db.Entity):
    """
        Базовый класс человека

        :param id: Идентификатор
        :type id: number
        :access id: dev
        :mod id dev: edit look

        :param username: Логин
        :type username: text
        :access username: dev
        :mod username dev: create edit look

        :param password: Пароль
        :type password: password
        :access password: dev
        :mod password dev: create

        :param name: Имя пользователя
        :type name: text
        :access name: dev
        :mod name dev: create edit look

        :param surname: Фамилия пользователя
        :type surname: text
        :access surname: dev
        :mod surname dev: create edit look

        :param email: Почта
        :type email: text
        :access email: dev
        :mod email dev: create edit look

        :param human_contacts: Контакты
        :type human_contacts: adding_field
        :access human_contacts: dev
        :mod human_contacts dev: create edit look

        :param photo: Ваша фотография
        :type photo: image
        :access photo: dev
        :mod photo dev: create edit look

        :param status: Статус
        :type status: text
        :access status: dev
        :mod status dev: create edit look

        :param description: Пару слов о себе
        :type description: text
        :access description: dev
        :mod description dev: create edit look

        :param scopes: настроить уровни доступа
        :type scopes: scopes
        :access scopes: dev
        :mod scopes dev: create edit look

        :param questions: Вашм вопросы
        :type questions: qu_select
        :access questions: dev
        :mod questions dev: look

        напрямую использоваться не должен
    """
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)  # login
    hash_password = Required(str, 8192)
    name = Required(str)
    surname = Required(str)
    email = Required(str, unique=True)
    human_contacts = Optional('HumanContacts')
    photo = Optional(str)
    status = Optional(str)
    description = Optional(str)
    scopes = Optional(Json)
    questions = Set('Question')


class Admin(Human):
    """
        Админ

        :access id: dev admin
        :mod id admin dev: edit look
        :mod id admin: look

        :access username: dev admin self
        :mod username self dev: create edit look
        :mod username admin: create look

        :access password: dev admin self
        :mod password self dev: create
        :mod password admin: create look

        :access name: dev admin self
        :mod name  self  dev: create edit look
        :mod name admin: create look

        :access surname: dev admin self
        :mod surname  self  dev: create edit look
        :mod surname admin: create look

        :access email: dev admin self
        :mod email  self dev: create edit look
        :mod email admin: create look

        :access human_contacts: dev admin self
        :mod human_contacts  self dev: create edit look
        :mod human_contacts admin: create look

        :access photo: dev admin self
        :mod photo  self dev: create edit look
        :mod photo admin: create look

        :access status: dev admin self
        :mod status  self dev: create edit look
        :mod status admin: create look

        :access description: dev admin self
        :mod description  self dev: create edit look
        :mod description admin: create look

        :access scopes: dev admin self
        :mod scopes  self dev: create edit look
        :mod scopes admin: create look

        :access questions: dev admin self
        :mod questions  self dev: create edit look
        :mod questions admin: create look


    """
    pass


class User(Human):
    """
        Участник, который может отправлять работы на конкурс

        :access id: dev admin self
        :mod id user admin dev: edit look

        :access username: dev admin self public
        :mod username user admin dev: create edit look
        :mod questions public: create


        :access password: dev admin self public
        :mod password user admin dev: create
        :mod questions public: create


        :access name: dev admin self public
        :mod name user admin dev: create edit look
        :mod questions public: create


        :access surname: dev admin self public
        :mod surname user admin dev: create edit look
        :mod questions public: create

        :access email: dev admin self public
        :mod email user admin dev: create edit look
        :mod questions public: create

        :access human_contacts: dev admin self
        :mod human_contacts user admin dev: create edit look

        :access photo: dev admin self public
        :mod photo user admin dev: create edit look
        :mod questions public: create

        :access status: dev admin self public
        :mod status user admin dev: create edit look
        :mod questions public: create

        :access description: dev admin self public
        :mod description user admin dev: create edit look
        :mod questions public: create

        :access scopes: dev admin self
        :mod scopes user admin dev: create edit look

        :access questions: dev admin self
        :mod questions user admin dev: create edit look


        :param date_of_birth: Дата рождения
        :type date_of_birth: date
        :access date_of_birth: dev admin self public
        :mod date_of_birth user dev admin: create edit look
        :mod questions public: create


        :param about_program: Что для вас программа?
        :type about_program: text
        :access about_program: dev admin self
        :mod about_program user dev admin: create edit look

        :param direction: Какое направление прогшраммы вы считаете главным для себя?
        :type direction: text
        :access direction: dev admin self
        :mod direction user dev admin: create edit look

        :param visible_about_program_field: Показывать этот отзыв на главной странице в разделе "Выпускники"?
        :type visible_about_program_field: bool
        :access visible_about_program_field: dev admin
        :mod visible_about_program_field dev admin: create edit look


        (если ему еще нет 18)
    """
    date_of_birth = Required(date)  # день рождения
    user_works = Set('UserWork')
    about_program = Optional(str)  # Отзыв о программе
    direction = Optional(str)  # с каким направлением себя ассоциирует участник
    visible_about_program_field = Required(bool, default='false')
    # будет ли отзыв участника о программе
    # отображаться на главной странице


class Smm(Human):
    """
        Пишет посты, занимается контентом сайта

        :access id: dev admin smm
        :mod id smm admin dev: edit look

        :access username: dev admin smm
        :mod username smm admin dev: create edit look

        :access password: dev admin smm
        :mod password smm admin dev: create

        :access name: dev admin smm
        :mod name smm admin dev: create edit look

        :access surname: dev admin smm
        :mod surname smm admin dev: create edit look

        :access email: dev admin smm
        :mod email smm admin dev: create edit look

        :access human_contacts: dev admin smm
        :mod human_contacts smm admin dev: create edit look

        :access photo: dev admin smm
        :mod photo smm admin dev: create edit look

        :access status: dev admin smm
        :mod status smm admin dev: create edit look

        :access description: dev admin smm
        :mod description smm admin dev: create edit look

        :access scopes: dev admin smm
        :mod scopes smm admin dev: create edit look

        :access questions: dev admin smm
        :mod questions smm admin dev: create edit look


        но не обладает правами админа
    """
    pass


class Developer(Human):
    """
        Разработчик

        :access id: dev
        :mod id self: look
        :mod id dev: edit look

        :access username: dev
        :mod username dev: look
        :mod username self: create edit look

        :access password: dev
        :mod password dev: create
        :mod password self: create

        :access name: dev
        :mod name dev: look
        :mod name self: create edit look

        :access surname: dev
        :mod surname dev: look
        :mod surname self: create edit look

        :access email: dev
        :mod email dev: look
        :mod email self: create edit look

        :access human_contacts: dev
        :mod human_contacts dev: look
        :mod human_contacts self: create edit look

        :access photo: dev
        :mod photo dev: look
        :mod photo self: create edit look

        :access status: dev
        :mod status dev: look
        :mod status self: create edit look

        :access description: dev
        :mod description dev: look
        :mod description self: create edit look

        :access scopes: dev
        :mod scopes dev: look
        :mod scopes self: create edit look

        :access questions: dev
        :mod questions dev: look
        :mod questions self: create edit look

    """
    pass


class HumanContacts(db.Entity):
    """
        Необязательные контакты человека

        :param phone: Ваш номер телефона
        :type phone: phone_number
        :access phone: dev admin self
        :mod phone self: create edit look
        :mod phone dev admin: look

        :param vk: Ссылка на ваш профиль вконтакте
        :type vk: url
        :access vk: dev admin self
        :mod vk self: create edit look
        :mod vk dev admin: look

        :param insagramm: Ссылка на ваш профиль в insagram
        :type insagramm: url
        :access insagramm: dev admin self
        :mod insagramm self: create edit look
        :mod insagramm dev admin: look

        :param facebook: Ссылка на ваш профиль в facebook
        :type facebook: url
        :access facebook: dev admin self
        :mod facebook self: create edit look
        :mod facebook dev admin: look

        :param telegram: Ссылка на ваш профиль в telegram
        :type telegram: url
        :access telegram: dev admin self
        :mod telegram self: create edit look
        :mod telegram dev admin: look

        :param home_adress: Ваш домашний адрес
        :type home_adress: text
        :access home_adress: dev admin self
        :mod home_adress self: create edit look
        :mod home_adress dev admin: look

    """
    human = PrimaryKey(Human)
    phone = Optional(str)
    vk = Optional(str)
    insagramm = Optional(str)
    facebook = Optional(str)
    home_adress = Optional(str)
    telegram = Optional(str)


class DirectionExpert(Human):
    """
        Проверяет работы детей на конкурсе

        :access id: dev admin smm
        :mod id expert admin dev: edit look

        :access username: dev admin smm
        :mod username expert admin dev: create edit look

        :access password: dev admin smm
        :mod password expert admin dev: create

        :access name: dev admin smm
        :mod name expert admin dev: create edit look

        :access surname: dev admin smm
        :mod surname expert admin dev: create edit look

        :access email: dev admin smm
        :mod email expert admin dev: create edit look

        :access human_contacts: dev admin smm
        :mod human_contacts expert admin dev: create edit look

        :access photo: dev admin smm
        :mod photo expert admin dev: create edit look

        :access status: dev admin smm
        :mod status expert admin dev: create edit look

        :access description: dev admin smm
        :mod description expert admin dev: create edit look

        :access scopes: dev admin smm
        :mod scopes expert admin dev: create edit look

        :access questions: dev admin smm
        :mod questions expert admin dev: create edit look

   """
    competition_directions = Set('CompetitionDirection')  # один эксперт может быть экспертом в нескольких направлениях


class Competition(db.Entity):
    """
        Конкурс типа НоваторВеб

        :param id: id
        :type id: number
        :access id: dev admin
        :mod id dev admin: create edit look

        :param name: Название конкурса
        :type name: text
        :access name: dev admin
        :mod name dev admin: create edit look

        :param start: дата и время начала
        :type start: datetime
        :access start: dev admin
        :mod start dev admin: create edit look

        :param end: дата и время окончания приёма работ на конкурс
        :type end: datetime
        :access end: dev admin
        :mod end dev admin: create edit look

        :param description: Описание конкурса
        :type description: text
        :access description: dev admin
        :mod description dev admin: create edit look

        :param document: Ркгламент проведения конкурса
        :type document: file
        :access document: dev admin
        :mod document dev admin: create edit look

    """
    id = PrimaryKey(int, auto=True)
    name = Required(str)  # Соревнование, такое как "Новатор Web"
    start = Required(datetime)  # Время начала конкурса
    end = Required(datetime)  # Время окончания конкурса
    description = Optional(str)
    competition_direction = Set('CompetitionDirection')
    document = Optional(str)  # ссылка на документ, регламентирующий конкурс


class Direction(db.Entity):
    """
        Направление конкурса, тмпа "IT" или "Design"

        :param name: Название направления (что-то вроде "Design" или "IT")
        :type name: text
        :access name: dev admin self
        :mod name dev admin: create edit look

        :param icon: Картинка направления
        :type icon: image
        :access icon: dev admin
        :mod icon dev admin: create edit look

        :param video_lessons: Видеоуроки по направлению
        :type video_lessons: video_lessons
        :access video_lessons: dev admin
        :mod video_lessons dev admin: create edit look

    """
    name = PrimaryKey(str)
    icon = Required(str)  # картинка направления
    competition_direction = Set('CompetitionDirection')
    video_lessons = Optional(Json)


class CompetitionDirection(db.Entity):
    """
        Задание по направлению на конкретный конкурс

        :param directions: Выберите направление, по которому будет задание
        :type directions: select
        :access questions: dev admin
        :mod questions dev admin: create edit look

        :param competition: Выберите конкурс, в рамках которого будет задание
        :type competition: select
        :access questions: dev admin
        :mod questions dev admin: create edit look

        :param direction_experts: Выберите экспертов, которые могут проверять направление
        :type direction_experts: multi_select
        :access questions: dev admin
        :mod questions dev admin: create edit look

    """
    directions = Required(Direction)
    competition = Required(Competition)
    tasks = Set('Task')
    direction_experts = Set(DirectionExpert)  # Направление конкурса может иметь нескольких проверяющих (экспертов)
    PrimaryKey(directions, competition)


class Task(db.Entity):
    """
        В одном направлении за конкурс может быть несколько этапов

        :param id: id
        :type id: number
        :access id: dev admin expert
        :mod id dev admin: edit look
        :mod id expert: look

        :param competition_direction: Выберите направление конкурса для этого задания
        :type competition_direction: select
        :access competition_direction: dev admin expert
        :mod competition_direction dev admin: create edit look
        :mod competition_direction expert: create edit look

        :param task_document: документ с заданием
        :type task_document: file
        :access task_document: dev admin expert
        :mod task_document dev admin: create edit look
        :mod task_document expert: create edit look

        :param description: Краткое описание задания
        :type description: text
        :access description: dev admin expert
        :mod description dev admin: create edit look
        :mod description expert: create edit look

        :param start: дата и время начала проведения этапа
        :type start: datetime
        :access start: dev admin expert
        :mod start dev admin: create edit look
        :mod start expert: create edit look

        :param end: дата и время окончания приёма работ на этот этап
        :type end: datetime
        :access end: dev admin expert
        :mod end dev admin: create edit look
        :mod end expert: create edit look

    """
    id = PrimaryKey(int, auto=True)
    competition_direction = Required(CompetitionDirection)
    criterions = Set('Criterion')
    task_document = Optional(str)  # путь к документу с заданием на этап
    description = Optional(str)
    start = Required(datetime)
    # Время начала
    # приёма работ на
    # конкретный этап
    end = Required(datetime)
    # Время окончания
    # приёма работ на
    # конкретный этап
    user_works = Set('UserWork')


class UserWork(db.Entity):
    """
        Работа участника на конкурс

        :param task: Выберите задание, на которое вы отправляете работу
        :type task: select
        :access task: dev admin user expert
        :mod task dev admin user: create edit look
        :mod task expert: look

        :param work: Вставьте ссылку на вашу работу (ее можно разместить, к примеру, на яндекс диске)
        :type work: url
        :access work: dev admin expert user
        :mod work dev admin user: create edit look
        :mod work expert: look

        :param mark_works: Оценки работ участников
        :type mark_works: select
        :access mark_works: dev admin expert user
        :mod mark_works dev admin expert: create edit look
        :mod mark_works user: look

        :param user: Чья это работа?
        :type user: select
        :access user: dev admin expert user
        :mod user dev admin expert: look
        :mod user user: look

        :param upload_date: Время последнего обновления
        :type upload_date: datetime
        :access upload_date: dev admin expert user
        :mod upload_date dev admin expert: look
        :mod upload_date user: look

        :param upload_date: Время последнего обновления
        :type upload_date: datetime
        :access upload_date: dev admin expert user
        :mod upload_date dev admin expert: edit look
        :mod upload_date user: look

    """
    mark_works = Set('MarkWork')
    # Каждая работа может
    # иметь оценки
    # по нескольким критериям
    user = Required(User)
    task = Required(Task)
    work = Optional(str)  # Ссылка на работу
    upload_date = Required(datetime, default=lambda: datetime.now())  # Дата загрузки
    mark = Optional(str)
    PrimaryKey(user, task)


class Criterion(db.Entity):
    """
        Критерий (один) для оценки работы

        :param id: id
        :type id: number
        :access id: dev admin expert
        :mod id dev: edit look
        :mod id admin expert: look

        :param task: Выберите задание, к которому принадлежит данный критерий
        :type task: select
        :access task: dev admin expert
        :mod task dev admin expert: create edit look

        :param name: Название критерия
        :type name: text
        :access name: dev admin expert
        :mod name dev admin expert: create edit look

        :param description: Описание критерия
        :type description: text
        :access description: dev admin expert
        :mod description dev admin expert: create edit look

        :param max_value: Максимальное количество баллов за критерий
        :type max_value: number
        :access max_value: dev admin expert
        :mod max_value dev admin expert: create edit look

        :param mark_works: Работы, оцененые по этому критерию
        :type mark_works: select
        :access mark_works: dev admin expert
        :mod mark_works dev admin expert: look
    """
    task = Required(Task)
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    max_value = Optional(float)
    mark_works = Set('MarkWork')  # Каждый критерий можно применить ко всем работам в направлении конкурса


class MarkWork(db.Entity):
    """
        Оценка работы на конкурс по определённому критерию

        :param criterion: По какому критерию эта оценка?
        :type criterion: select
        :access criterion: dev admin expert
        :mod criterion dev admin expert: create edit look

        :param user_work: Выберите работу для оценки
        :type user_work: select
        :access user_work: dev admin expert
        :mod user_work dev admin expert: create edit look

        :param value: Количество баллов
        :type value: number
        :access value: dev admin expert
        :mod value dev admin expert: create edit look


        Оценка по конкретному критерию однозначно
        определяется определяется критерием и работой участника
    """
    criterion = Required(Criterion)
    user_work = Required(UserWork)
    value = Required(int)  # оценка работы на конкурс по определённому критерию
    PrimaryKey(criterion, user_work)


class Page(db.Entity):
    """
        Страница сайта

        :param id: id
        :type id: number
        :access id: dev admin smm
        :mod id dev admin smm: edit look

        :param page_url: Ссылка, по которой будет распологаться страница
        :type page_url: text
        :access page_url: dev admin smm
        :mod page_url dev admin smm: create edit look

        :param page_path: имя файла страницы
        :type page_path: text
        :access page_path: dev admin smm
        :mod page_path dev admin smm: create edit look

        :param is_header: Отображать ли страницу в верхнем меню?
        :type is_header: bool
        :access is_header: dev admin smm
        :mod is_header dev admin : create edit look
        :mod is_header smm: look

        :param visible: Смогут ли пользователи видеть страницу (эту, как и всю прочую, информациб потом можно отредактировать)?
        :type visible: bool
        :access visible: dev admin smm
        :mod visible dev admin smm: create edit look

        :param root_page: Будет ли страница подстраницей какой-нибудь части верхнего меню?
        :type root_page: select
        :access root_page: dev admin smm
        :mod root_page dev admin smm: create edit look

        :param child_pages: какие подстраницы у этой страницы?
        :type child_pages: select
        :access child_pages: dev admin smm
        :mod child_pages dev admin smm: look

        :param title: Заголовок страницы
        :type title: text
        :access title: dev admin smm
        :mod title dev admin smm: create edit look

        :param questions: выберите вопросы, которые будут отображаться внизу этой страницы
        :type questions: multi_select
        :access questions: dev admin smm
        :mod questions dev admin smm: create edit look

        :param page_type: Выберите тип страницы, к примеру "события"
        :type page_type: text
        :access page_type: dev admin smm
        :mod page_type dev admin smm: create edit look

        пока что будет использоваться только для заголовков
    """
    id = PrimaryKey(int, auto=True)
    page_url = Optional(str)  # ссылка, на которой будет располагаться эта страница
    page_path = Optional(str)  # Путь, по которому лежит html-файл этой страницы
    is_header = Required(bool, default='false')
    # Если True,
    # то страница будет  включена в меню сайта
    visible = Required(bool, default='false')  # показывать ли страницу на сайте или "спрятать"
    child_pages = Set('Page', reverse='root_page')
    # каждая страница может иметь
    #  несколько дочерних страниц
    # К примеру: страница "события" может иметь дочерние страницы dominno и teengrad
    root_page = Optional('Page', reverse='child_pages')
    title = Optional(str)  # заголовок страницы
    questions = Set('Question')
    page_type = Optional(str)


class Question(db.Entity):
    """
        Вопросы участников

        :param id: id
        :type id: number
        :access id: dev admin
        :mod id dev admin: edit look

        :param question_title: О чем вопрос в двух словах?
        :type question_title: text
        :access question_title: public dev admin
        :mod question_title dev admin: create edit look
        :mod question_title public: create look

        :param question: Текст вопроса
        :type question: text
        :access question: public dev admin
        :mod question dev admin: create edit look
        :mod question public: create look

        :param answer: Ответ
        :type answer: text
        :access answer: public dev admin
        :mod answer dev admin: create edit look
        :mod answer public: look

        :param pages: Страницы, на которых будет отображаться этот вопрос в разделе "частозадаваемые вопросы"
        :type pages: text
        :access answer: public dev admin
        :mod pages dev admin: create edit look
        :mod pages public: look

        :param answer_email: email, на который следует отправить ответ, если вопрос задан не авторизированным пользователем
        :type answer_email: email
        :access answer: public dev admin
        :mod answer_email dev admin: create edit look
        :mod answer_email public: look

        :param human: Человек, задавший вопрос
        :type human: select
        :access answer: public dev admin
        :mod human dev admin: look
        :mod human public: look

        :param was_read: Этот вопрос был прочитан?
        :type was_read: bool
        :access answer: public dev admin
        :mod was_read dev admin: create edit look
        :mod was_read public: look

        :param was_answered: На этот вопрос был дан ответ?
        :type was_answered: bool
        :access answer: public dev admin
        :mod was_answered dev admin: create edit look
        :mod was_answered public: look

    """
    id = PrimaryKey(int, auto=True)
    question_title = Optional(str)
    # тема вопроса
    # или краткое описание
    question = Required(str)
    answer = Optional(str)
    pages = Set(Page)
    # на какие страницы может быть
    # добавлен вопрос как чатозадаваемый
    #  (по умолчанию - ни на какие)
    answer_email = Optional(str)
    # Почта для ответа
    # (если пользователь не зарегистрирован)
    human = Optional(Human)
    # если пользователь залогинен,
    # то ответ приходит ему в личный кабинет
    was_read = Required(bool, default='false')  # Вопрос прочитан?
    was_answered = Required(bool, default='false')  # ответ на вопрос отправлен?


class SimpleEntity(db.Entity):
    """
        Используется чтобы не создавать "простые" сущности БД на "каждый чих"

        :param key: Название новой колонки в базе данных
        :type key: text
        :access key: dev admin
        :mod key dev admin: create edit look

        :param data: структура колонки БД
        :type data: db_json
        :access data: dev admin
        :mod data dev admin: create edit look

        тут будут помещены Партнеры программы, социальные сети и т.д.
    """
    key = PrimaryKey(str, auto=True)
    data = Optional(Json)


class News(Page):
    """
        Новость

        :param auto_publish: Введите время публикации новости
        :type auto_publish: datetime
        :access auto_publish: dev admin smm
        :mod auto_publish dev admin smm: create edit look

        :param image: Главное изображение в новости
        :type image: image
        :access image: dev admin smm
        :mod image dev admin smm: create edit look

        :param author: Автор новости
        :type author: text
        :access author: dev admin smm
        :mod author dev admin smm: create edit look

        :param description: Краткое описание новост
        :type description: text
        :access description: dev admin smm
        :mod description dev admin smm: create edit look

    """
    auto_publish = Optional(datetime)  # Тата автоматической публикации
    image = Optional(str)
    author = Optional(str)
    description = Optional(str)  # краткое описание новости