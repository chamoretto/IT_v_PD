from app.db._change_db._db_additions._base_additions import _raw_m


def important_field_for_print(cls):
    return ["id", "title", "visible", "image"]


_raw_m.db.entities["News"].only_classmetod(important_field_for_print)
