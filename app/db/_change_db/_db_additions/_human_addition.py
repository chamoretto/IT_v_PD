from app.db._change_db._db_additions._base_additions import _raw_m


def important_field_for_print(cls):
    return ["id", "username", "name", "surname", "photo"]


_raw_m.db.entities["Human"].only_classmetod(important_field_for_print)


def before_insert(self):
    """ вызывается до создания объекта """

    from app.utils.utils_of_security import scopes_to_db

    if not bool(self.scopes):
        self.scopes = scopes_to_db.get(self.__class__, [])


_raw_m.db.entities["Human"].only_func(before_insert)
