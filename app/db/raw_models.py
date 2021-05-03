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