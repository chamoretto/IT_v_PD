from app.db._change_db._db_additions._base_additions import _raw_m
from app.db._change_db._db_additions._human_addition import important_field_for_print

_raw_m.db.entities["DirectionExpert"].only_classmetod(important_field_for_print)
