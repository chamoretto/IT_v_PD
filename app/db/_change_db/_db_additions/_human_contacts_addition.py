from app.db._change_db._db_additions._base_additions import _raw_m


def important_field_for_print(cls):
    return ["human", "vk", "phone"]


_raw_m.db.entities["HumanContacts"].only_classmetod(important_field_for_print)
