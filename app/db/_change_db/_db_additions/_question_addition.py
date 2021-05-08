from app.db._change_db._db_additions._base_additions import _raw_m


def important_field_for_print(cls):
    return ["id", "question_title", "human", "was_read", "was_answered"]

_raw_m.db.entities["Question"].only_classmetod(important_field_for_print)