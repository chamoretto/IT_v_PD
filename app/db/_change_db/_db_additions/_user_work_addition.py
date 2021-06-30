from app.db._change_db._db_additions._base_additions import _raw_m


def important_field_for_print(cls):
    return ["user", "task", "mark"]


_raw_m.db.entities["UserWork"].only_classmetod(important_field_for_print)
