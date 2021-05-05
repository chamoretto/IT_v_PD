from datetime import date
from pony.orm import *


db = Database()


class Human(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)  # login
    hash_password = Required(str, 8192)
    name = Required(str)
    surname = Required(str)
    email = Required(str, unique=True)
    contacts = Optional('Contacts')
    photo = Optional(str)
    status = Optional(str)
    description = Optional(str)


class Admin(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)  # login
    hash_password = Required(str, 8192)
    name = Required(str)
    surname = Required(str)
    email = Required(str, unique=True)
    # contacts = Optional('Contacts')
    photo = Optional(str)
    status = Optional(str)
    description = Optional(str)


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)  # login
    hash_password = Required(str, 8192)
    name = Required(str)
    surname = Required(str)
    email = Required(str, unique=True)
    # contacts = Optional('Contacts')
    photo = Optional(str)
    status = Optional(str)
    description = Optional(str)
    age = Required(date)


class Smm(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)  # login
    hash_password = Required(str, 8192)
    name = Required(str)
    surname = Required(str)
    email = Required(str, unique=True)
    # contacts = Optional('Contacts')
    photo = Optional(str)
    status = Optional(str)
    description = Optional(str)


class Developer(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)  # login
    hash_password = Required(str, 8192)
    name = Required(str)
    surname = Required(str)
    email = Required(str, unique=True)
    # contacts = Optional('Contacts')
    photo = Optional(str)
    status = Optional(str)
    description = Optional(str)


class Contacts(db.Entity):
    human = PrimaryKey(Human)
    phone = Optional(str)
    vk = Optional(str)
    insagramm = Optional(str)
    facebook = Optional(str)
    home_adress = Optional(str)
    telegram = Optional(str)


class DirectionExpert(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)  # login
    hash_password = Required(str, 8192)
    name = Required(str)
    surname = Required(str)
    email = Required(str, unique=True)
    # contacts = Optional('Contacts')
    photo = Optional(str)
    status = Optional(str)
    description = Optional(str)


# db.generate_mapping()

from app.utils.pydantic_security import HumanInDB
from app.utils.utils_of_security import get_password_hash

dict_db = {"Admin": []}


class BaseDb:

    @classmethod
    def exists(cls, **kwargs):
        if any([all([getattr(i, key) == val for key, val in kwargs.items()]) for i in dict_db.get(cls.__name__, [])]):
            return True
        return False

    @classmethod
    def get(cls, **kwargs):
        return [i for i in dict_db.get(cls.__name__, []) if all([getattr(i, key) == val for key, val in kwargs.items()])][0]

    def __init__(self, **kwargs):
        # self.me = HumanInDB(**kwargs)
        self.__dict__ = kwargs
        dict_db[self.__class__.__name__] = dict_db.get(self.__class__.__name__, []) + [self]


    def to_dict(self, **kwargs):
        return dict(self.__dict__)

# class Admin(BaseDb):
#     pass
#
# Admin(
#     id=1,
#     username="admin",
#     hash_password=get_password_hash("admin"),
#     name="Daniil",
#     surname="D'yachkov",
#     email="rkbcu@mail.ru",
# )