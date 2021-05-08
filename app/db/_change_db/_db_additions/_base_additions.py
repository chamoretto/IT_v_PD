from typing import List

from pony.orm import db_session, show, select

from app.db._change_db import _raw_models as _raw_m
from app.db._change_db._db_additions.tools_for_addition import AddArrtInDbClass

_start = set(globals())


# @classmethod
# def db_show(cls, width=None):
#     class MyStream:
#
#         def __init__(self):
#             self.content = ""
#
#         def write(self, string: str):
#             self.content += string
#
#         def flush(self):
#             pass
#
#         def get_result(self):
#             return self.content
#
#     my_stream = MyStream()
#     show(cls, width=width, stream=my_stream)
#
#     return my_stream.get_result()


@classmethod
def important_field_for_print(cls):
    return []


def get_entity_html(self, keys):
    # language=HTML
    return f"<tr>{''.join(['<td>' + str(getattr(self, key)) + '</td>' for key in keys])}</tr>"


@classmethod
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
    except Exception as e:
        print(e)
        # language=HTML
        return f"<table><caption>{cls.__name__}</caption>" \
               f"<thead><tr><th>Не удалось найти сущност в базе данных</th></tr></thead>" \
               f"<tbody></tbody></table>"
    body_table = [i.get_entity_html(data) for i in select((ent for ent in cls))[:]]

    body_table = '\n'.join(body_table)
    print(data)
    # language=HTML
    return f"<table><caption>{cls.__name__}</caption>" \
           f"<thead><tr>{''.join(['<th>' + key + '</th>' for key in data])}</tr></thead>" \
           f"<tbody>{body_table}</tbody></table>"


added_params = set(globals()) - _start - {"_start"}

entities_code = {}  # Тут будет находиться код сущностей БД в удобном виде
for name, ent in _raw_m.db.entities.items():
    ent.__bases__ = (tuple(list(ent.__bases__) + [AddArrtInDbClass])
                     if AddArrtInDbClass not in list(ent.__bases__)
                     else tuple(list(ent.__bases__)))
    # entities_code[ent] = db_ent_to_dict(ent)
    # entities_code[name] = entities_code[ent]

    [setattr(ent, added_param, globals()[added_param]) for added_param in added_params]
    AddArrtInDbClass.change_field[name] = AddArrtInDbClass.change_field.get(name, set()) | set(added_params)

print(AddArrtInDbClass.change_field)

if __name__ == "__main__":
    from app.dependencies import *

    with db_session:
        print(_raw_m.Page.get_entities_html())
