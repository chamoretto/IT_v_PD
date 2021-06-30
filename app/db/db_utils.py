from pony.orm import db_session, commit
from datetime import date

from app.db import models
from app.db.models import db
from app.settings.config import cfg, DB_PATH, DB_BACKUPS
from app.utils.utils_of_security import get_password_hash


def old_connect_with_db(db_path=DB_PATH, deep=0, db_l=db):
    """
    Создает соединение с БД для Pony ORM версии 0.73

    :param db_path: путь к БД
    :param deep: глубина рекурсии
    :param db_l: объект БД
    :return:
    """
    from os.path import isfile, split, join
    from os import remove, rename
    from sys import exit
    from time import ctime
    from shutil import copy as shutil_copy

    if deep > 5:
        print("в коннекте с базой данных наблюдается большая рекурсия, значит что-то идет не так")
        exit()

    if not isfile(db_path):
        db_l.bind(provider=cfg.get("db", "type"), filename=db_path, create_db=True)
        db_l.generate_mapping(create_tables=True)

        """
                db_l.connect(allow_auto_upgrade=True,
                     create_tables=True,
                     create_db=True,
                     provider=cfg.get("db", "type"),
                     filename=db_path)
        """

        print("create db")
    else:

        try:
            db_l.bind(provider=cfg.get("db", "type"), filename=db_path)
            db_l.generate_mapping()
        except Exception as e:
            print("при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n", e)
            print("попытка исправить.....")
            try:
                db_l.bind(
                    provider=cfg.get("db", "type"),
                    filename=db_path,
                    create_tables=True,
                )
                db_l.generate_mapping()
                print("получилось")
            except Exception as e:
                print("Создаём бекап а затем удаляем БД")
                t = ctime().split()[1:]
                t[0], t[1], t[2] = t[2], t[1], t[0]
                copy_name = shutil_copy(db_path, DB_BACKUPS)
                new_name = join(split(copy_name)[0], "_".join(t).replace(":", "-") + "_" + split(db_path)[1])
                rename(copy_name, new_name)
                print("создан бекап:", new_name)
                print("Удалена исходная база данных, создаём новую")
                remove(db_path)
                print("\n=========================================\n\n\t\tдля создания новой БД перезапустите код.....")
                print("\n=========================================")
                exit()


def _connect_with_db(db_path=DB_PATH, deep=0, db_l=db):
    """
    Создает соединение с БД для Pony ORM версии 0.8

    :param db_path: путь к БД
    :param deep: глубина рекурсии
    :param db_l: объект БД
    :return:
    """
    from os.path import isfile, split, join
    from os import remove, rename
    from sys import exit
    from time import ctime
    from shutil import copy as shutil_copy

    db_path = str(db_path)
    if deep > 5:
        print("в коннекте с базой данных наблюдается большая рекурсия, значит что-то идет не так")
        exit()
    print(db_path, isfile(db_path), not isfile(db_path))
    if not isfile(db_path):
        db_l.connect(
            allow_auto_upgrade=True,
            create_tables=True,
            create_db=True,
            provider=cfg.get("db", "type"),
            filename=db_path,
        )
        print("create db_1")
    else:

        try:
            db_l.connect(allow_auto_upgrade=True, provider=cfg.get("db", "type"), filename=db_path)
        except Exception as e:
            print("при создании бд произошла какая-то ошибка (видимо, структура БД была изменена)\n", e)
            print("попытка исправить.....")
            try:
                db_l.connect(
                    allow_auto_upgrade=True,
                    create_tables=True,
                    # create_db=True,
                    provider=cfg.get("db", "type"),
                    filename=db_path,
                )
                print("получилось")
            except Exception as e:
                print("Начинаем миграцию")
                t = ctime().split()[1:]
                t[0], t[1], t[2] = t[2], t[1], t[0]
                copy_name = shutil_copy(db_path, DB_BACKUPS)
                new_name = join(split(copy_name)[0], "_".join(t).replace(":", "-") + "_" + split(db_path)[1])
                rename(copy_name, new_name)
                print("создан бекап:", new_name)
                print("Удалена исходная база данных, создаём новую")
                remove(db_path)
                # controller_migration_version(db_path)
                print("\n=========================================\n\n\t\tдля создания новой БД перезапустите код.....")
                print("\n=========================================")
                exit()
                # connect_with_db(db_path=db_path, deep=deep + 1)


def connect_with_db(db_path=DB_PATH, deep=0, db_l=db):
    try:
        raise Exception()
        _connect_with_db(db_path=db_path, deep=deep, db_l=db_l)
    except Exception:
        old_connect_with_db(db_path=db_path, deep=deep, db_l=db_l)
    finally:
        try:
            with db_session:
                if not models.Admin.exists(username="admin"):
                    models.Admin(
                        username="admin",
                        hash_password=get_password_hash("admin"),
                        name="Daniil",
                        surname="D'yachkov",
                        email="ad_rkbcu@mail.ru",
                    )
                    commit()
                if not models.Developer.exists(username="developer"):
                    models.Developer(
                        username="developer",
                        hash_password=get_password_hash("developer"),
                        name="Daniil",
                        surname="D'yachkov",
                        email="de_rkbcu@mail.ru",
                    )
                    commit()
                if not models.Smm.exists(username="smmer"):
                    models.Smm(
                        username="smmer",
                        hash_password=get_password_hash("smmer"),
                        name="Daniil",
                        surname="D'yachkov",
                        email="sm_rkbcu@mail.ru",
                    )
                    commit()
                if not models.DirectionExpert.exists(username="direction_expert"):
                    models.DirectionExpert(
                        username="direction_expert",
                        hash_password=get_password_hash("direction_expert"),
                        name="Daniil",
                        surname="D'yachkov",
                        email="dr_rkbcu@mail.ru",
                    )
                    commit()
                if not models.User.exists(username="user"):
                    models.User(
                        username="user",
                        hash_password=get_password_hash("user"),
                        name="Daniil",
                        surname="D'yachkov",
                        email="us_rkbcu@mail.ru",
                        date_of_birth=date(2004, 4, 4),
                    )
                    commit()
            print("роли для теста созданы")
        except Exception as e:
            print("При создании стартовых сущностей возникла непредвиденная ошибка", e)
            # models.Pam(id=1, id_2="3")
            # commit()
            # models.Pampam(id=1, pam=models.Pam[1, "3"])
            # commit()
            # print(models.Pampam[1, 1, "3"])


def open_db_session():
    try:
        # with db_session:
        yield ""
    finally:
        pass
