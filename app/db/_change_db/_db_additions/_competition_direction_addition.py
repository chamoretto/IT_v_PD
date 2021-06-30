from app.db._change_db._db_additions._base_additions import _raw_m


def important_field_for_print(cls):
    return ["competition", "directions"]


_raw_m.db.entities["CompetitionDirection"].only_classmetod(important_field_for_print)
