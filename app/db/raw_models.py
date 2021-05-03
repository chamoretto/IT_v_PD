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


class Admin(Human):
    pass


class User(Human):
    age = Required(date)


class Smm(Human):
    pass


class Developer(Human):
    pass


class Contacts(db.Entity):
    human = PrimaryKey(Human)
    phone = Optional(str)
    vk = Optional(str)
    insagramm = Optional(str)
    facebook = Optional(str)
    home_adress = Optional(str)
    telegram = Optional(str)


class DirectionExpert(Human):
    pass


# db.generate_mapping()