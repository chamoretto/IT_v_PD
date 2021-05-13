import enum

from app.pydantic_models import db_models as pd
from app.pydantic_models import unique_db_field_models as pk_pd
from app.pydantic_models import unique_db_field_models as pk_pd
from app.pydantic_models import input_ent as inp_pd
from app.pydantic_models import output_ent as out_pd
from app.pydantic_models import only_primarykey_fields_model as only_pk

from datetime import date
from datetime import datetime
from pony.orm import *

db = Database()


class Human(db.Entity):
    """
        Базовый класс человека

        :param id: Идентификатор
        :type id: number
        :param username: Логин
        :type username: text
        :param password: Пароль
        :type password: password
        :param name: Имя пользователя
        :type name: text
        :param surname: Фамилия пользователя
        :type surname: text
        :param email: Почта
        :type email: text
        :param human_contacts: Контакты
        :type human_contacts: adding_field
        :param photo: Ваша фотография
        :type photo: image
        :param status: Статус
        :type status: text
        :param description: Пару слов о себе
        :type description: text

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

    @classmethod
    def important_field_for_print(cls):
        return ["id", "username", "name", "surname", "photo"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class Admin(Human):
    """
    Админ

    """
    pass

    @classmethod
    def important_field_for_print(cls):
        return ["id", "username", "name", "surname", "photo"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class User(Human):
    """
        Участник, который может отправлять работы на конкурс

        :param date_of_birth: Дата рождения
        :type date_of_birth: date
        :param about_program: Что для вас программа?
        :type about_program: text
        :param direction: Какое направление прогшраммы вы считаете главным для себя?
        :type direction: text

        (если ему еще нет 18)
    """
    date_of_birth = Required(date)  # день рождения
    user_works = Set('UserWork')
    about_program = Optional(str)  # Отзыв о программе
    direction = Optional(str)  # с каким направлением себя ассоциирует участник
    visible_about_program_field = Required(bool, default='false')
    # будет ли отзыв участника о программе
    # отображаться на главной странице

    @classmethod
    def important_field_for_print(cls):
        return ["id", "username", "name", "surname", "photo"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class Smm(Human):
    """
        Пишет посты, занимается контентом сайта

        но не обладает правами админа
    """
    pass

    @classmethod
    def important_field_for_print(cls):
        return ["id", "username", "name", "surname", "photo"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class Developer(Human):
    """
        Разработчик

    """
    pass

    @classmethod
    def important_field_for_print(cls):
        return ["id", "username", "name", "surname", "photo"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class HumanContacts(db.Entity):
    """
        Необязательные контакты человека

        :param phone: Ваш номер телефона
        :type phone: phone_number
        :param vk: Ссылка на ваш профиль вконтакте
        :type vk: url
        :param insagramm: Ссылка на ваш профиль в insagram
        :type insagramm: url
        :param facebook: Ссылка на ваш профиль в facebook
        :type facebook: url
        :param telegram: Ссылка на ваш профиль в telegram
        :type telegram: url
        :param home_adress: Ваш домашний адрес
        :type home_adress: text

    """
    human = PrimaryKey(Human)
    phone = Optional(str)
    vk = Optional(str)
    insagramm = Optional(str)
    facebook = Optional(str)
    home_adress = Optional(str)
    telegram = Optional(str)

    @classmethod
    def important_field_for_print(cls):
        return ["human", "vk", "phone"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class DirectionExpert(Human):
    """
        Проверяет работы детей на конкурсе

    """
    competition_directions = Set('CompetitionDirection')  # один эксперт может быть экспертом в нескольких направлениях

    @classmethod
    def important_field_for_print(cls):
        return ["id", "username", "name", "surname", "photo"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class Competition(db.Entity):
    """
        Конкурс типа НоваторВеб

        :param id: id
        :type id: number
        :param name: Название конкурса
        :type name: text
        :param start: дата и время начала
        :type start: datetime
        :param end: дата и время окончания приёма работ на конкурс
        :type end: datetime
        :param description: Описание конкурса
        :type description: text
        :param document: Ркгламент проведения конкурса
        :type document: file
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str)  # Соревнование, такое как "Новатор Web"
    start = Required(datetime)  # Время начала конкурса
    end = Required(datetime)  # Время окончания конкурса
    description = Optional(str)
    competition_direction = Set('CompetitionDirection')
    document = Optional(str)  # ссылка на документ, регламентирующий конкурс

    @classmethod
    def important_field_for_print(cls):
        return ["name", "start", "end"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class Direction(db.Entity):
    """
        Направление конкурса, тмпа "IT" или "Design"

        :param name: Название направления (что-то вроде "Design" или "IT")
        :type name: text
        :param icon: Картинка направления
        :type icon: image
        :param video_lessons: Видеоуроки по направлению
        :type video_lessons: video_lessons
    """
    name = PrimaryKey(str)
    icon = Required(str)  # картинка направления
    competition_direction = Set('CompetitionDirection')
    video_lessons = Optional(Json)

    @classmethod
    def important_field_for_print(cls):
        return ["icon", "name"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class CompetitionDirection(db.Entity):
    """
        Задание по направлению на конкретный конкурс

        :param directions: Выберите направление, по которому будет задание
        :type directions: select
        :param competition: Выберите конкурс, в рамках которого будет задание
        :type competition: select
        :param direction_experts: Выберите экспертов, которые могут проверять направление
        :type direction_experts: multi_select
    """
    directions = Required(Direction)
    competition = Required(Competition)
    tasks = Set('Task')
    direction_experts = Set(DirectionExpert)  # Направление конкурса может иметь нескольких проверяющих (экспертов)
    PrimaryKey(directions, competition)

    @classmethod
    def important_field_for_print(cls):
        return ["competition", "directions"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class Task(db.Entity):
    """
        В одном направлении за конкурс может быть несколько этапов

        :param id: id
        :type id: number
        :param competition_direction: Выберите направление конкурса для этого задания
        :type competition_direction: select
        :param task_document: документ с заданием
        :type task_document: file
        :param description: Краткое описание задания
        :type description: text
        :param start: дата и время начала проведения этапа
        :type start: datetime
        :param end: дата и время окончания приёма работ на этот этап
        :type end: datetime
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

    @classmethod
    def important_field_for_print(cls):
        return ["id", "competition_direction", "start", "end", "photo"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class UserWork(db.Entity):
    """
        Работа участника на конкурс

        :param task: Выберите задание, на которое вы отправляете работу
        :type task: select
        :param work: Вставьте ссылку на вашу работу (ее можно разместить, к примеру, на яндекс диске)
        :type work: url
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

    @classmethod
    def important_field_for_print(cls):
        return ["user", "task", "mark"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class Criterion(db.Entity):
    """
        Критерий (один) для оценки работы

        :param id: id
        :type id: number
        :param task: Выберите задание, к которому принадлежит данный критерий
        :type task: select
        :param name: Название критерия
        :type name: text
        :param description: Описание критерия
        :type description: text
        :param max_value: Максимальное количество баллов за критерий
        :type max_value: number
    """
    task = Required(Task)
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    description = Optional(str)
    max_value = Optional(float)
    mark_works = Set('MarkWork')  # Каждый критерий можно применить ко всем работам в направлении конкурса

    @classmethod
    def important_field_for_print(cls):
        return ["id", "competition_direction", "name", "max_value"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class MarkWork(db.Entity):
    """
        Оценка работы на конкурс по определённому критерию

        :param criterion: По какому критерию эта оценка?
        :type criterion: select
        :param user_work: Выберите работу для оценки
        :type user_work: select
        :param value: Количество баллов
        :type value: number

        Оценка по конкретному критерию однозначно
        определяется определяется критерием и работой участника
    """
    criterion = Required(Criterion)
    user_work = Required(UserWork)
    value = Required(int)  # оценка работы на конкурс по определённому критерию
    PrimaryKey(criterion, user_work)

    @classmethod
    def important_field_for_print(cls):
        return ["criterion", "user_work", "value"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class Page(db.Entity):
    """
        Страница сайта

        :param id: id
        :type id: number
        :param page_url: Ссылка, по которой будет распологаться страница
        :type page_url: text
        :param page_path: имя файла страницы
        :type page_path: text
        :param is_header: Отображать ли страницу в верхнем меню?
        :type is_header: bool
        :param visible: Смогут ли пользователи видеть страницу?
        :type visible: bool
        :param root_page: Будет ли страница подстраницей какой-нибудь части верхнего меню?
        :type root_page: select
        :param title: Заголовок страницы
        :type title: number
        :param questions: выберите вопросы, которые будут отображаться внизу этой страницы
        :type questions: multi_select

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
    def important_field_for_print(cls):
        return ["id", "title", "page_url", "is_header", "visible"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


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
    def important_field_for_print(cls):
        return ["id", "question_title", "human", "was_read", "was_answered"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class SimpleEntity(db.Entity):
    """Используется чтобы не создавать "простые" сущности БД на "каждый чих"

тут будут помещены Партнеры программы, социальные сети и т.д."""
    key = PrimaryKey(str, auto=True)
    data = Optional(Json)

    @classmethod
    def important_field_for_print(cls):
        return ["key"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


class News(Page):
    """Новость"""
    auto_publish = Optional(datetime)  # Тата автоматической публикации
    image = Optional(str)
    author = Optional(str)
    description = Optional(str)  # краткое описание новости

    @classmethod
    def important_field_for_print(cls):
        return ["id", "title", "visible", "image"]

    def get_entity_html(self, keys):
        # language=H TML
        data = f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
               f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
               f'<i class="far fa-trash-alt"></i></a></td>' \
               f'<td><a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
        # print(data)
        return data

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
               f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Посмотреть</td><td>Редактировать</td><td>Удалить</td></tr></thead>" \
               f"<tbody>{body_table}</tbody></table>"

    def key_as_part_query(self):
        _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
        _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
        return _dict


setattr(db, 'EntitiesEnum', enum.Enum('DynamicEnum', {key: key for key, val in db.entities.items()}))
