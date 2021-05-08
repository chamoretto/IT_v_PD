from app.db._change_db._db_additions._base_additions import _raw_m


def important_field_for_print(cls):
    return ["id", "competition_direction", "start", "end", "photo"]

_raw_m.db.entities["Task"].only_classmetod(important_field_for_print)