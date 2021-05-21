from typing import Dict, List, Tuple, Any, Callable
from itertools import chain
from functools import reduce
from os.path import exists
from os import mkdir

from app.db.models import db
from app.db._change_db._create_models import db_ent_to_dict, StringDB, code_from_db_and_docs, AllInfoStr, AccessType, \
    AccessMode, FieldHtmlType
from app.settings.config import AUTO_PYDANTIC_MODELS, split, join
from app.db._change_db._create_models import DbDocs, info_from_docs
from app.pydantic_models.pony_to_pydantic_rules import *
from app.pydantic_models.standart_methhods_redefinition import PydanticValidators


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
    new_types_dict = dict()
    for name, val in pk_for_pydantic.items():
        new_types.append(f"Pk{name} = Union[{', '.join(val)}]\n")
        new_types_dict[f"Pk{name}"] = f"Union[{', '.join(val)}]"
    new_types.append('\n')
    for name, val in pk_for_pydantic.items():
        new_types.append(f"OptionalPk{name} = Union[{', '.join(val + ['None'])}]\n")
        new_types_dict[f"OptionalPk{name}"] = f"Union[{', '.join(val + ['None'])}]"
    new_types.append('\n')
    for name, val in pk_for_pydantic.items():
        new_types.append(f"SetPk{name} = Set[Union[{', '.join(val)}]]\n")
        new_types_dict[f"SetPk{name}"] = f"Set[Union[{', '.join(val)}]]"
    new_types = "".join(new_types)
    new_types = ""  # новые типы не используются
    return new_types + "\n\n", pk_for_pydantic, new_types_dict


def create_pd_class_body(class_name: str, code: List[StringDB], new_types_dict: dict[str, str]) -> str:
    """Создаёт тела pydantic-класса"""

    #       приводим тип атрибута к типу, понятному pydantic
    [[val(i) for key, val in change_attr_type.items() if key(i, db)] for i in code]
    #       приводим тип поля PonyORM к типу, понятному pydantic
    [[val(i) for key, val in type_db_param_to_text.items() if key(i)] for i in code]
    #       устанавливаем значения по умолчанию
    [[val(i) for key, val in change_default.items() if key(i)] for i in code]

    [setattr(i, "param_type", new_types_dict[i.param_type]) for i in code if i.param_type in new_types_dict]
    pd_class_body = "".join([db_string_to_pydantic_string(i) for i in code])

    return pd_class_body


def create_header_pd_file(entities: List[db.Entity], code, create_roles=False) -> str:
    add_types = set(entities) - set(code)
    data = '# -*- coding: utf-8 -*-\n\n' \
           '\n\"\"\" Этот код генерируется автоматически,\n' \
           'функцией create_pd_models файла app/db/create_pydantic_models.py\n' \
           '-------!!!!!! Ни одно изменение не сохранится в этом файле. !!!!!-----\n\n' \
           'Тут объявляются pydantic-модели, в которых присутствуют все сущности БД\n' \
           'и все атрибуты сущностей\"\"\"\n\n'

    data += 'from typing import Set, Union, List, Dict, Tuple, ForwardRef\n' \
            'from typing import Optional, Literal, Any\n' \
            'from pydantic import Json, root_validator, validator\n' \
            'from datetime import date, datetime, time\n\n' \
            'from app.pydantic_models.standart_methhods_redefinition import BaseModel, as_form\n' \
            'from app.pydantic_models.standart_methhods_redefinition import PydanticValidators\n'
    if create_roles:
        if create_roles == AccessMode.CREATE:
            data += '\n'.join([f'from app.pydantic_models.gen.input_ent import {i}' for i in add_types]) + '\n'
        else:
            data += '\n'.join([f'from app.pydantic_models.gen.output_ent import {i}' for i in add_types]) + '\n'
    data += 'from app.settings.config import HOME_DIR\n\n\n'

    for entity in code:
        data += f'{entity} = ForwardRef("{entity}")\n'
    return data + "\n"


def create_pd_class(class_name: str, code: List[AllInfoStr], new_types_dict: dict[str, str]) -> str:
    data = f""
    data += f"class {class_name}(BaseModel):\n"
    data += create_pd_class_body(class_name, code, new_types_dict)
    data += ''.join([PydanticValidators[i] for i in code])
    data += '\n' \
            '\tclass Config:\n' \
            '\t\torm_mode = True\n\n\n'
    return data


def create_footer_pd_file(entities: List[db.Entity], code) -> str:
    data = ""
    for entity in code:
        data += f'{entity}.update_forward_refs()\n'
    data += "\n\nif __name__ == '__main__':\n\tfrom os import chdir\n\n\tchdir(HOME_DIR)"
    return data


def add_db_docs_with_code(name: str, code: StringDB, ent: db.Entity):
    pass


def create_pd_models(
        file_name: str = AUTO_PYDANTIC_MODELS,
        filter_func: Callable[[str, AllInfoStr, ...], bool] = lambda *a, **k: True,
        map_param_funcs: list[Callable[[str, AllInfoStr, ...], Tuple[str, AllInfoStr]]] = [
            lambda key, val, *a, **k: (key, val)],
        class_filter: Callable[[dict[str, AllInfoStr], ...], bool] = lambda *a, **k: True,
        create_roles=False
):
    pd_db: Dict[str, Tuple[Dict[str, AllInfoStr], Dict[str, Dict[List[str], List[str]]], Any, db.Entity]] = dict()

    # =======! Получаем код сущности !=======
    for name, ent in db.entities.items():
        code, p_k = code_from_db_and_docs(ent)
        code.pop("Discriminator", "")
        code.pop("classtype", "")
        for map_param_func in map_param_funcs:
            code = dict([map_param_func(key, val, p_k) for key, val in code.items()])
        pd_db[name] = [code, p_k, ent.__bases__[0], ent]

    # =======! Обрабатываем сложные типы !=======
    pd_db = get_nice_pk(pd_db)
    new_types_code, pk_for_pydantic, new_types_dict = create_pk_types(pd_db)

    # =======! Фильтруем код сущности !=======
    for name, [code, p_k, parent, ent] in pd_db.copy().items():
        if not class_filter(code, p_k):
            del pd_db[name]
            continue
        code: dict[str, AllInfoStr] = {key: val for key, val in code.items() if filter_func(key, val, p_k)}
        if class_filter(code, p_k):
            pd_db[name] = [code, p_k, ent.__bases__[0], ent]
        else:
            del pd_db[name]

    # ======! Превращаем класс PonyORM в pydantic-класс !=======
    file_code: str = create_header_pd_file(db.entities, pd_db, create_roles=create_roles)
    file_code += new_types_code
    for name, [code, p_k, parent, ent] in pd_db.items():
        file_code += create_pd_class(name, code.values(), new_types_dict)
    file_code += create_footer_pd_file(db.entities, pd_db)
    if not exists(split(file_name)[0]):
        mkdir(split(file_name)[0])
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(file_code)


def change_hash_to_password_field(key: str, val: AllInfoStr, *a, **k):
    if key == "password":
        key = "password"
        setattr(val, "name", "password")
        setattr(val, "param_type", "str")
        print('+========================================', key, val)
    return key, val


if __name__ == '__main__':

    create_pd_models(
        filter_func=lambda key, val, *a, **k: not val.is_not_db,
        map_param_funcs=[
            lambda key, val, *a, **k: (
                [setattr(val, "db_type", "Optional"), (key, val)][1] if val.other_params.get("auto") else (key, val))
        ]
    )  # Обычнве модели из базы данных
    create_pd_models(  # модель только с уникальными параметрами
        file_name=join(split(AUTO_PYDANTIC_MODELS)[0], "unique_db_field_models.py"),
        filter_func=lambda key, val, p_k, *a, **k:
        (val.other_params.get("unique") or val.is_primary_key or any(val.name in j for j in p_k)),
        map_param_funcs=[
            lambda key, val, *a, **k: (
                [setattr(val, "db_type", "Optional"), (key, val)][1] if val.other_params.get("auto") else (key, val))
        ]
    )

    create_pd_models(
        file_name=join(split(AUTO_PYDANTIC_MODELS)[0], "input_ent.py"),
        filter_func=lambda key, val, p_k, *a, **k: not val.other_params.get("auto"),
        map_param_funcs=[
            change_hash_to_password_field,
            lambda key, val, *a, **k: (
                [setattr(val, "db_type", "Optional"), (key, val)][1] if val.other_params.get("auto") else (
                    key, val))

        ])  # Сущности, которые будут приниматься с сайта
    create_pd_models(  # сущности, которые должен возвращать сайт
        file_name=join(split(AUTO_PYDANTIC_MODELS)[0], "output_ent.py"),
        filter_func=lambda key, val, *a, **k: all(i not in key for i in ["password", "hash"]) and val.html_type != FieldHtmlType.PASSWORD)

    create_pd_models(
        file_name=join(split(AUTO_PYDANTIC_MODELS)[0], "only_primarykey_fields_model.py"),
        filter_func=lambda key, val, p_k, *a, **k:
        (val.is_primary_key or any(val.name in j for j in p_k))
    )
    create_pd_models(
        filter_func=lambda key, val, *a, **k: not val.is_not_db,
        file_name=join(split(AUTO_PYDANTIC_MODELS)[0], "all_optional_models.py"),
        map_param_funcs=[
            lambda key, val, *a, **k: (setattr(val, "db_type", "Optional"), (key, val))[
                1] if val.db_type != "Set" else (key, val)
        ]
    )

    base_path = [split(AUTO_PYDANTIC_MODELS)[0]]
    true_print = lambda val, *a: not (print(val.class_name, *val.dict().items(), *a, " ", sep='\n') if val.name == "password" else False)
    true_print = lambda *a: True
    for role in AccessType:
        # print('+!!!!!!!!---', role, [role])

        for mode in AccessMode:

            # print("-089654678")
            maps = []
            filters = []
            if mode == AccessMode.CREATE:
                maps = [change_hash_to_password_field,
                        lambda key, val, *a, **k: (
                            [setattr(val, "db_type", "Optional"), (key, val)][1] if val.other_params.get("auto") else (
                                key, val))
                        ]
                filters = [lambda key, val, p_k, *a, **k: not val.other_params.get("auto")]
            else:
                filters = [lambda key, val, p_k, *a, **k: val.html_type != FieldHtmlType.PASSWORD]
            create_pd_models(
                file_name=join(*base_path, str(role), f'{role}_{mode}.py'),
                filter_func=lambda key, val, *a, **k: true_print(val) and (r := val.access.get(role)) and true_print(val, r, mode) and mode in r and true_print(val) and all(i(key, val, *a, **k) for i in filters) and true_print(val),
                class_filter=lambda code, p_k, *a, **k: bool(code),
                create_roles=mode,
                map_param_funcs=maps

                # map_param_funcs=[
                #     lambda key, val, *a, **k: (setattr(val, "db_type", "Optional"), (key, val))[
                #         1] if val.db_type != "Set" else (key, val)
                # ]
            )
            # print('+_**************')
