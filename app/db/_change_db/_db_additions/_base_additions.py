from typing import List
from functools import reduce

from pony.orm import db_session, show, select

from app.db._change_db import _raw_models as _raw_m
from app.db._change_db._db_additions._tools_for_addition import AddArrtInDbClass
from app.pydantic_models import only_primarykey_fields_model as only_pk
from app.utils.html_utils import nice_table_page

_start = set(globals())



@classmethod
def important_field_for_print(cls):
    return []


def get_entity_html(self, keys):
    # language=H TML
    data =  f'<tr>{"".join(["<td>" + str(getattr(self, key)) + "</td>" for key in keys])}' \
           f'<td><a href="/db/{self.__class__.__name__}/edit?{self.key_as_part_query()}"><i class="far fa-edit"></i></a>' \
           f'<a href="/db/{self.__class__.__name__}/delete?{self.key_as_part_query()}" class="color-error">' \
           f'<i class="far fa-trash-alt"></i></a>' \
           f'<a href="/db/{self.__class__.__name__}/look?{self.key_as_part_query()}"><i class="far fa-eye-slash"></i></a></td></tr>'
    # print(data)
    return data


def key_as_part_query(self):
    _dict = dict(getattr(only_pk, self.__class__.__name__).from_orm(self))
    _dict = "&".join([f"{key}={val}" for key, val in _dict.items()])
    return _dict



@classmethod
@nice_table_page
def get_entities_html(cls, *keys):
    try:
        keys = list(keys)
        if not bool(keys):
            keys = list(cls.important_field_for_print())
        if not bool(keys):
            keys = None
        data = list(select(ent for ent in cls).random(limit=1)[:1][0].to_dict(with_collections=False, only=keys).keys())
        print('----', data)
        # data = data.to_dict(with_collections=False, only=keys).keys()
    except IndexError as e:
        print("Произошла ошибка IndexError в классе", cls, "при генерации таблицы сущностей", e)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
           f"<thead><tr><th>Похоже в этой колонке базы данных нет ни одной сущности (БД пуста)</th></tr></thead>" \
           f"<tbody></tbody></table>"
    except Exception as e:
        print("Произошла ошибка в классе", cls, "при генерации таблицы сущностей", e)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
               f"<tbody></tbody></table>"
    body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

    body_table = '\n'.join(body_table)
    print(data)
    # language=HTML
    return f"<table><caption>{cls.__name__}</caption>" \
           f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}<td>Операции</td></tr></thead>" \
           f"<tbody>{body_table}</tbody></table>"




added_params = set(globals()) - _start - {"_start"}

new_funcs = {
    "important_field_for_print": "",
    "get_entity_html": "",
    "get_entities_html": "",
    "key_as_part_query": ""
}

entities_code = {}  # Тут будет находиться код сущностей БД в удобном виде
for name, ent in _raw_m.db.entities.items():
    ent.__bases__ = (tuple(list(ent.__bases__) + [AddArrtInDbClass])
                     if AddArrtInDbClass not in list(ent.__bases__)
                     else tuple(list(ent.__bases__)))
    # entities_code[ent] = db_ent_to_dict(ent)
    # entities_code[name] = entities_code[ent]

    [setattr(ent, added_param, globals()[added_param]) for added_param in added_params]
    AddArrtInDbClass.change_field[ent] = AddArrtInDbClass.change_field.get(ent, dict()) | new_funcs
    # AddArrtInDbClass.change_field_types[name] = "@classmethod"

print(AddArrtInDbClass.change_field)

if __name__ == "__main__":
    from app.dependencies import *

    with db_session:
        print(_raw_m.Page.get_entities_html())
