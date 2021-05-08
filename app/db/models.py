from datetime import date
from datetime import datetime
from pony.orm import *

db = Database()


class Human(db.Entity):
    """Базовый класс человека

    :param db_path: путь к БД
    :type db_path: путь к БД
    :param deep: глубина рекурсии
    :param db_l: объект БД

напрямую использоваться не должен"""
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

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class Admin(Human):
    pass

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class User(Human):
    """Участник, который может отправлять работы на конкурс

(если ему еще нет 18)"""
    user_works = Set('UserWork')
    about_program = Optional(str)  # Отзыв о программе
    direction = Optional(str)  # с каким направлением себя ассоциирует участник
    visible_about_program_field = Required(bool, default='false')
    # будет ли отзыв участника о программе
    # отображаться на главной странице
    date_of_birth = Required(date)  # день рождения

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class Smm(Human):
    """Пишет посты, занимается контентом сайта

но не обладает правами админа"""
    pass

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class Developer(Human):
    pass

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class HumanContacts(db.Entity):
    human = PrimaryKey(Human)
    phone = Optional(str)
    vk = Optional(str)
    insagramm = Optional(str)
    facebook = Optional(str)
    home_adress = Optional(str)
    telegram = Optional(str)

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class DirectionExpert(Human):
    """Проверяет работы детей на конкурсе"""
    competition_directions = Set('CompetitionDirection')  # один эксперт может быть экспертом в нескольких направлениях

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class Competition(db.Entity):
    """Конкурс типа НоваторВеб"""
    name = PrimaryKey(str)
    start = Required(datetime)  # Время начала конкурса
    end = Required(datetime)  # Время окончания конкурса
    description = Optional(str)
    competition_direction = Set('CompetitionDirection')
    document = Optional(str)  # ссылка на документ, регламентирующий конкурс

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class Direction(db.Entity):
    """направление конкурса, тмпа "IT" или "Design" """
    name = PrimaryKey(str)
    icon = Required(str)  # картинка направления
    competition_direction = Set('CompetitionDirection')
    video_lessons = Optional(Json)

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class CompetitionDirection(db.Entity):
    """Задание по направлению
на конкретный конкурс"""
    directions = Required(Direction)
    competition = Required(Competition)
    tasks = Set('Task')
    direction_experts = Set(DirectionExpert)  # Направление конкурса может иметь нескольких проверяющих (экспертов)
    criterions = Set('Criterion')  # каждое направление может иметь несколько критериев оценки
    PrimaryKey(directions, competition)

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class Task(db.Entity):
    """В одном направлении за конкурс может быть несколько этапов"""
    id = PrimaryKey(int, auto=True)
    competition_direction = Required(CompetitionDirection)
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

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class UserWork(db.Entity):
    """Работа участника на конкурс"""
    mark_works = Set('MarkWork')
    # Каждая работа может
    # иметь оценки
    # по нескольким критериям
    user = Required(User)
    task = Required(Task)
    work = Optional(str)  # Ссылка на работу
    upload_date = Required(datetime)  # Дата загрузки
    mark = Optional(str)
    PrimaryKey(user, task)

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class Criterion(db.Entity):
    """критерий (один)
для оценки работы"""
    id = PrimaryKey(int, auto=True)
    competition_direction = Required(CompetitionDirection)
    name = Required(str)
    description = Optional(str)
    max_value = Optional(float)
    mark_works = Set('MarkWork')  # Каждый критерий можно применить ко всем работам в направлении конкурса

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class MarkWork(db.Entity):
    """оценка работы на конкурс по определённому критерию

Оценка по конкретному критерию однозначно
определяется определяется критерием и работой участника"""
    criterion = Required(Criterion)
    user_work = Required(UserWork)
    value = Required(int)  # оценка работы на конкурс по определённому критерию
    PrimaryKey(criterion, user_work)

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class Page(db.Entity):
    """Страница сайта

    :param db_path: путь к БД
    :type db_path: путь к БД
    :param deep: глубина рекурсии
    :param db_l: объект БД
    :return:

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
    # К примеру: страница "события" может иметь дочерние страницы djminno и teengrad
    root_page = Optional('Page', reverse='child_pages')
    title = Optional(str)  # заголовок страницы
    questions = Set('Question')

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class Question(db.Entity):
    """Вопросы участников"""
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

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class SimpleEntity(db.Entity):
    """Используется чтобы не создавать "простые" сущности БД на "каждый чих"

тут будут помещены Партнеры программы, социальные сети и т.д."""
    key = PrimaryKey(str, auto=True)
    data = Optional(Json)

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []


class News(Page):
    """Новость"""
    auto_publish = Optional(datetime)  # Тата автоматической публикации
    image = Optional(str)
    author = Optional(str)
    description = Optional(str)  # краткое описание новости

    @classmethod
    def get_entities_html(cls, *keys):
        try:
            keys = list(keys)
            if not bool(keys):
                keys = list(cls.important_field_for_print())
            if not bool(keys):
                keys = None
            data = list(
                select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
            print('----', data)
            # data = data.to_dict(with_collections=False, only=keys).keys()
        except Exception as e:
            print(e)
            # language=HTML
            return f"<table><caption>{cls.__name__}</caption>" \
                   f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
                   f"<tbody></tbody></table>"
        body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

        body_table = '\n'.join(body_table)
        print(data)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def get_entity_html(self, keys):
        # language=HTML
        return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"

    @classmethod
    def important_field_for_print(cls):
        return []
