from typing import Dict, List, Tuple, Any
from itertools import chain
from functools import reduce

from app.db.models import db
from app.db._change_db._create_models import db_ent_to_dict, StringDB
from app.settings.config import AUTO_PYDANTIC_MODELS

# =======! Правила изменения типа pony-атрибутов !=======
change_attr_type_rules = {
    "Json": "Json",
    "time": "time",
    "datetime": "datetime"
}
change_attr_type = {
    lambda i: i.param_type in change_attr_type_rules:
        lambda i: setattr(i, 'param_type', change_attr_type_rules[i.param_type]),
    lambda i: i.param_type in db.entities and i.db_type != "Optional":
        lambda i: setattr(i, 'param_type', "Pk" + i.param_type),
    lambda i: i.param_type in db.entities and i.db_type == "Optional":
        lambda i: setattr(i, 'param_type', "OptionalPk" + i.param_type),
}

# =======! Интерпретируем типы полей БД в pydantic-язык !=======
change_db_field = {
    "PrimaryKey": "",
    "Required": "",
    "Optional": "Optional",
    "Set": "Set",
    "Discriminator": "Optional",
}
type_db_param_to_text = {
    lambda i: i.db_type in change_db_field: lambda i: setattr(i, 'db_type', change_db_field[i.db_type]),
}

# =======! Устанавливаем значения по умолчанию !=======
change_default_rules = {
    "": None,
    "PrimaryKey": None,
    "Required": None,
    "Optional": "None",
    "Set": "[]"
}
change_default = {
    lambda i: i.default is not None and "lambda" not in i.default and i.param_type == "bool":
        lambda i: setattr(i, 'default', ("True" if any(j in i.default.lower() for j in ["1", "true"]) else "False")),
    lambda i: i.default is not None and "lambda" not in i.default and i.param_type in ["int", "float"]:
        lambda i: setattr(i, 'default', reduce(lambda st, i: st.replace(i), ["'", '"'], i.default)),
    lambda i: i.default is not None and "lambda" not in i.default and i.param_type == "Json":
        lambda i: setattr(i, 'default', '"' + i.default + '"'),
    lambda i: i.default is None or "lambda" in i.default:
        lambda i: setattr(i, 'default', change_default_rules[i.db_type]),
}


def db_string_to_pydantic_string(data: StringDB):
    string = f"\t{data.name}: "
    if bool(data.db_type):
        string += f"{data.db_type}[{data.param_type}]"
    else:
        string += f"{data.param_type}"
    if data.default is not None:
        string += f" = {data.default}"
    return string + "\n"


def get_nice_pk(
        pd_db: Dict[str, Tuple[Any, Dict[str, Dict[List[str], List[str]]], Any, Any]]) -> \
        Dict[str, Tuple[Any, Dict[str, List[Tuple[List[str], List[str]]]], Any, Any]]:
    """
        Переводит pk из сложных типов (db.Entity) в простые (к примеру: [int, str, str])
        
        :param pd_db: 
        :return: 
    """

    processed_pk: Dict[str, Any] = {}
    while True:
        stop = True
        for name, [_, pk, *_] in pd_db.items():
            for key, val in filter(lambda j: any(j1 in db.entities for j1 in j[1]), pk.items()):
                pd_db[name][1][key] = [(processed_pk[i] if i in processed_pk else i) for i in val]
                stop = False
            if all(val not in db.entities for _, vals in pk.items() for val in vals):
                processed_pk[name] = pk.values()

        if stop:
            break
    for name, [_, pk, *_] in pd_db.items():
        pd_db[name][1] = [[list(key), list(chain(*[([i] if type(i) == str else list(*chain(i))) for i in pk[key]]))] for
                          key in pk]
        while any(type(val) != str for _, vals in pd_db[name][1] for val in vals):
            pd_db[name][1] = [[key, reduce(lambda arr, i: arr + ([i] if type(i) == str else list(i)), val, [])] for
                              [key, val] in pd_db[name][1]]
    return pd_db


def create_pk_types(pd_db):
    # =======! Обрабатываем сложные типы !=======

    pk_for_pydantic: Dict[str, List[str]] = {}

    for name, [code, pk, parent, ent] in pd_db.items():
        pk_for_pydantic[name] = ["Tuple[" + ", ".join(
            [change_attr_type_rules.get(val, val) for val in vals]
        ) + "]" for [_, vals] in pk if len(vals) != 1]

        pk_for_pydantic[name] += [change_attr_type_rules.get(val[0], val[0]) for [_, val] in pk if len(val) == 1]
        pk_for_pydantic[name] += [name]

    # =======! Добавляем дополнительные типы !=======
    for name, val in pk_for_pydantic.items():
        pk_for_pydantic[name] += []

    # =======! Выносим большие типы в отдельные переменные !=======
    new_types = []
    for name, val in pk_for_pydantic.items():
        new_types.append(f"Pk{name} = Union[{', '.join(val)}]\n")
    new_types.append('\n')
    for name, val in pk_for_pydantic.items():
        new_types.append(f"OptionalPk{name} = Union[{', '.join(val + ['None'])}]\n")
    new_types = "".join(new_types)

    return new_types + "\n\n", pk_for_pydantic


def create_pd_class_body(class_name: str, code: List[StringDB]) -> str:
    """Создаёт тела pydantic-класса"""

    #       приводим тип атрибута к типу, понятному pydantic
    [[val(i) for key, val in change_attr_type.items() if key(i)] for i in code]
    #       приводим тип поля PonyORM к типу, понятному pydantic
    [[val(i) for key, val in type_db_param_to_text.items() if key(i)] for i in code]
    #       устанавливаем значения по умолчанию
    [[val(i) for key, val in change_default.items() if key(i)] for i in code]

    pd_class_body = "".join([db_string_to_pydantic_string(i) for i in code])

    return pd_class_body


def create_header_pd_file(entities: List[db.Entity]) -> str:
    data = '# -*- coding: utf-8 -*-\n\n' \
           '\n\"\"\" Этот код генерируется автоматически,\n' \
           'функцией create_pd_models файла app/db/create_pydantic_models.py\n' \
           '-------!!!!!! Ни одно изменение не сохранится в этом файле. !!!!!-----\n\n' \
           'Тут объявляются pydantic-модели, в которых присутствуют все сущности БД\n' \
           'и все атрибуты сущностей\"\"\"\n\n'

    data += 'from typing import Set, Union, List, Dict, Tuple, ForwardRef\n' \
            'from typing import Optional, Literal, Any\n' \
            'from pydantic import Json\n' \
            'from datetime import date, datetime, time\n\n' \
            'from app.pydantic_models.standart_methhods_redefinition import BaseModel\n' \
            'from app.settings.config import HOME_DIR\n\n\n'

    for entity in entities:
        data += f'{entity} = ForwardRef("{entity}")\n'
    return data + "\n"


def create_pd_class(class_name: str, code: List[StringDB]) -> str:
    data = f"class {class_name}(BaseModel):\n"
    data += create_pd_class_body(class_name, code)
    data += '\n' \
            '\tclass Config:\n' \
            '\t\torm_mode = True\n\n\n'
    return data


def create_footer_pd_file(entities: List[db.Entity]) -> str:
    data = ""
    for entity in entities:
        data += f'{entity}.update_forward_refs()\n'
    data += "\n\nif __name__ == '__main__':\n\tfrom os import chdir\n\n\tchdir(HOME_DIR)"
    return data


def create_pd_models():
    pd_db: Dict[str, Tuple[Dict[str, StringDB], Dict[str, Dict[List[str], List[str]]], Any, db.Entity]] = {}

    # =======! Получаем код сущности !=======
    for name, ent in db.entities.items():
        code, p_k = db_ent_to_dict(ent)
        code.pop("Discriminator", "")
        code.pop("classtype", "")
        pd_db[name] = [code, p_k, ent.__bases__[0], ent]

    # =======! Обрабатываем сложные типы !=======
    pd_db = get_nice_pk(pd_db)
    new_types_code, pk_for_pydantic = create_pk_types(pd_db)

    # ======! Превращаем класс PonyORM в pydantic-класс !=======
    file_code: str = create_header_pd_file(db.entities)
    file_code += new_types_code
    for name, [code, p_k, parent, ent] in pd_db.items():
        file_code += create_pd_class(name, code.values())

    file_code += create_footer_pd_file(db.entities)

    with open(AUTO_PYDANTIC_MODELS, "w", encoding='utf-8') as f:
        print(file_code, file=f)


if __name__ == '__main__':
    create_pd_models()
