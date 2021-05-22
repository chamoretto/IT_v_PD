from typing import Tuple, Dict, List, Any, Optional, Callable
from functools import reduce
import enum
from collections import defaultdict

import inspect
from pydantic import root_validator

from app.settings.config import HOME_DIR, join
from app.pydantic_models.standart_methhods_redefinition import BaseModel, AccessType, AccessMode
from app.db._change_db._raw_models import db
from app.db._change_db import _raw_models
# from app.db._change_db._db_additions._base_additions import *
from app.db._change_db._all_db_additions import AddArrtInDbClass


@enum.unique
class FieldHtmlType(enum.Enum):
    TEXT = "text"
    NUMBER = "number"
    SELECT = "select"
    MULTI_SELECT = "multi_select"
    FILE = "file"
    IMAGE = "image"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    BOOL = "bool"
    PASSWORD = "password"
    ADDING_FIELD = "adding_field"
    PHONE_NUMBER = "phone_number"
    URL = "url"
    VIDEO_LESSONS = "video_lessons"
    SCOPES = "scopes"
    QUESTION_SELECT = "qu_select"
    EMAIL = "email"
    DB_JSON = "db_json"

    def __str__(self):
        return self.value

    @classmethod
    def get_obj(cls, val: str):
        if val in cls._value2member_map_:
            return cls._value2member_map_[val]
        print(val)
        raise AttributeError


class StringDB(BaseModel):
    """Олицетворяет одну строку в классе сузности Pony"""

    name: str  # имя поля (атрибута)
    db_type: str  # Set, Optional, Required, PrimaryKey
    param_type: str  # тип параметра, записываемого в БД
    default: Any = None  # параметр по умолчанию
    other_params: dict  # другие параметры
    is_primary_key: bool = False  #


class DbDocs(BaseModel):
    """
        описание БД из документации к коду


    """
    name: str
    description: Optional[str]
    html_type: Optional[FieldHtmlType]
    access: dict[AccessType, list[AccessMode]] = dict()
    required: bool = False
    class_name: str
    placeholder: str = ""
    default: Any = None
    is_entity: bool = False
    is_set: bool = False


class AllInfoStr(StringDB, DbDocs):
    name: str  # имя поля (атрибута)
    db_type: Optional[str]  # Set, Optional, Required, PrimaryKey
    param_type: Optional[str]  # тип параметра, записываемого в БД
    default: Any = None  # параметр по умолчанию
    other_params: dict = dict()  # другие параметры
    is_primary_key: bool = False  #
    is_not_db: bool = False  # если такой параметр есть только в документации

    @root_validator
    def check_passwords_match(cls, values: dict):
        if "db_type" not in values or values['db_type'] is None:
            values["is_not_db"] = True
            if "is_set" in values and values["is_set"]:
                values["db_type"] = "Set"
            elif "required" in values and values["is_set"]:
                values["db_type"] = "Required"
            else:
                values["db_type"] = "Optional"
        return values


def normalize_code(code: str) -> str:
    """
        Не используется. Удаляет из кода комментарии различного рода

        Ситуации с '''#dfgdfg''', #''', "#" (и подобные)
        не обрабатываются.
        Если скобка не закрыта, то код склеивает
        текущую строку со следующей, в надежде,
        что скобка закроется
    """

    comment_type = None
    result = []
    code = (i.split("#")[0].strip() for i in code.split('\n'))
    code = filter(bool, code)
    brackets_stack = 0
    for ind, char in enumerate(code):
        try:
            if comment_type is None:
                if char == '"' and code[ind + 1] == '"' and code[ind + 2] == '"':
                    comment_type = '"'
                elif char == "'" and code[ind + 1] == "'" and code[ind + 2] == "'":
                    comment_type = "'"
            elif comment_type == '"':
                if char == '"' and code[ind - 1] == '"' and code[ind - 2] == '"':
                    comment_type = None
            elif comment_type == "'":
                if char == "'" and code[ind - 1] == "'" and code[ind - 2] == "'":
                    comment_type = None
        finally:
            if comment_type is None:
                if char == "(":
                    brackets_stack += 1
                elif char == ")":
                    brackets_stack -= 1
                if not (char == "\n" and brackets_stack != 0):
                    result.append(char)

    return "".join(result)


def db_ent_to_dict(ent: db.Entity) -> Tuple[
    Dict[str, StringDB],
    Dict[str, Dict[
        List[str],
        List[str]
    ]]
]:
    """
    Генерирует представление класса БД в виде кода

    :param ent: Класс сущности, код которого будет трансформироваться
    :type ent: db.Entity
    :return: кодтеж, где первый элемент - словарь с кодом сущности
                (key: название поля, value: преобразованный код)
                а второй - словарь с primaryKey, где key: имя primaryKey, value: тип primaryKey
    :return type: Tuple[
        Dict[str, StringDB], - код
        Dict[str, - ключ - имя сущности
            Dict[
                List[str], - имена primaryKey-полей
                List[str] - типы primaryKey-полей
            ]
        ]
    ]

    В проекте имеется необходимость иметь доступ непосредственно к коду
    сущности БД (для построения другого файла и нетолько). Данная функция реализует
    этот функционал. В последствие, каждый атрибут из сущности БД представляется в виде
    pydantic-класса StringDB. Вся сущность объединяется в словарь с ключем
     - имя атрибуда в сущности Pony и соответствующим объектом StringDB.
     Также для каждой сущности возвращается словарь с primaryKey базы данных
     и типами этих primaryKey в БД
    """

    code = [i.strip() for i in ent.describe().split('\n')]
    p_k = [i for i in code if 'PrimaryKey' in i]
    code = (i.split('=') for i in code if '=' in i)
    code = ((i[0].strip(), '='.join(i[1:]).split('(')) for i in code)
    code = ((i[0], i[1][0].strip(), i[1][1].strip(')').split(',')) for i in code)

    code = ((i[0], i[1], i[2][0], [j.strip().split('=') for j in i[2][1:] if "=" in j]) for i in code)
    code = ((i[0], i[1], i[2], {j[0].strip(): j[1].strip() for j in i[3]}) for i in code)
    code = {i[0]: StringDB(
        name=i[0],
        db_type=i[1],
        param_type=reduce(lambda string, ch: string.replace(ch, ''), [i[2], '"', "'"]),
        default=i[3].pop('default', None),
        other_params=i[3],
        is_primary_key=i[1] == 'PrimaryKey'
    ) for i in code}

    simple_p_k = [i.split('=')[0].strip() for i in p_k if '=' in i]
    simple_p_k = {(i,): (code[i].param_type,) for i in simple_p_k}
    complex_p_k = [i.split('(')[1].strip(')').strip().split(',') for i in p_k if '=' not in i]
    complex_p_k = {tuple([j.strip() for j in i]): [code[j.strip()].param_type for j in i] for i in complex_p_k}
    simple_p_k.update(complex_p_k)
    return code, simple_p_k


def create_db_models():
    header_file = inspect.getsource(_raw_models).split('class')[0]
    header_file = "import enum\n" \
                  "from typing import Any\n\n" \
                  "try:\n" \
                  "\tfrom app.pydantic_models.gen import db_models as pd\n" \
                  "\tfrom app.pydantic_models.gen import unique_db_field_models as pk_pd\n" \
                  "\tfrom app.pydantic_models.gen import unique_db_field_models as pk_pd\n" \
                  "\tfrom app.pydantic_models.gen import input_ent as inp_pd\n" \
                  "\tfrom app.pydantic_models.gen import output_ent as out_pd\n" \
                  "except ImportError as e:\n" \
                  "\tprint('произошла ошибка при импорте моделей pydantic. По всей видимости в них ошибка', e)\n" \
                  "from app.pydantic_models.gen import only_primarykey_fields_model as only_pk\n" \
                  "from app.utils.html_utils import nice_table_page\n" \
                  "from app.pydantic_models.response_models import TableCell\n\n" + header_file

    classes: Dict[str: str] = {}
    for name, ent in db.entities.items():
        classes[name] = inspect.getsource(ent)
        classes[name] += "\n\n"
        add_func = [[decorator] + inspect.getsource(
            getattr(ent, i)
        ).split('\n') for i, decorator in AddArrtInDbClass.change_field[ent].items()]
        add_func = ["\n".join(["\t" + j for j in i]) for i in add_func]
        classes[name] += "\n\n".join([i for i in add_func])

    file_code = header_file
    file_code += "\n\n\n".join(list(classes.values()))
    file_code += "\n\nsetattr(db, 'EntitiesEnum', enum.Enum('DynamicEnum', {key: key for key, val in db.entities.items()}))"
    with open(join(HOME_DIR, "db", "models.py"), "w", encoding='utf-8') as f:
        print(file_code, file=f)


def get_doc(ent: db.Entity):
    if ent.__doc__:
        return "\n".join(
            [get_doc(parent) for parent in ent.__bases__ if parent.__name__ in db.entities]) + "\n" + ent.__doc__
    return ""


def get_access_dict(role_list: list[str]):
    if type(role_list) != list:
        role_list = [role_list]
    return {AccessType.get_obj(i): [] for i in role_list}


def full_access_dict(role_list: list[str], mode_list: list[str]):
    if type(mode_list) != list:
        mode_list = [mode_list]
    if type(role_list) != list:
        role_list = [role_list]
    mode_list = [AccessMode.get_obj(i) for i in mode_list]
    return {AccessType.get_obj(i): mode_list[:] for i in role_list}


def get_new_access(new_access: dict[AccessType, list[AccessMode]],
                   old_access: dict[AccessType, list[AccessMode]] = dict()):
    return old_access | new_access


def info_from_docs(ent: db.Entity) -> dict[str, DbDocs]:
    """
        Берёт информацию из документации к сущности БД и превращает ее в класс DbDocs

    """

    from app.pydantic_models.gen import db_models_for_create as pd

    keys_convertor: dict[str, str] = {
        "type": "html_type",
        "param": "description",
        "access": "access",
        "mod": "access",
    }
    vals_convertor: dict[str, Callable] = defaultdict(lambda: str)
    vals_convertor.update(dict(
        type=FieldHtmlType.get_obj,
        access=get_access_dict,
        mod=get_new_access,
    ))

    good_start: list[str] = [":mod" ":access", ":param", ":type"]
    pd_ent = getattr(pd, ent.__name__)
    # print(pd_ent)
    all_ent_docs: dict[str, DbDocs] = defaultdict(lambda: DbDocs(name=n.strip(), class_name=ent.__name__))

    all_docs = [i.strip() for i in get_doc(ent).split("\n")]
    # print(*all_docs, sep="\n")
    all_docs = [i[1:].split(":") for i in all_docs if not print(i) and bool(i) and not print(i) and any(
        i.strip().startswith(j) or i.strip().startswith(":mod") or i.strip().startswith(":access") for j in
        good_start) and not print(i)]
    # print(*all_docs, sep="\n")
    all_docs = ([t.split()] + [i for i in d.strip().split()] for [t, d] in all_docs)

    code, pk = db_ent_to_dict(ent)

    for [[t, n, *other], *d] in all_docs:
        obj: DbDocs = all_ent_docs[n.strip()]
        # print(t, n, other, d)
        if t not in ["access", "mod"]:
            d = ' '.join(d)
        if bool(other):  # mod
            print(other)
            d = full_access_dict(other, d)
            old_access = obj.access
            all_ent_docs[n.strip()] = DbDocs(**(obj.dict(exclude_unset=True) |
                                                {keys_convertor[t]: vals_convertor[t](d, old_access)}))
        else:  # type, param, access
            all_ent_docs[n.strip()] = DbDocs(**(obj.dict(exclude_unset=True) |
                                                {keys_convertor[t]: vals_convertor[t](d)}))

    for name, doc in all_ent_docs.items():
        # print(name, *doc.dict().items(), sep='\n')
        # print()
        if code.get(name):
            doc.required = code[name].db_type in ["PrimaryKey", "Required"]
            doc.is_set = not doc.required and code[name].db_type in ["Set"]
            doc.default = code.get(name).default
            # print(ent.__name__, name, doc.default)
            doc.is_entity = any(i in code[name].param_type for i in db.entities)
        else:
            doc.required = code.get(name, True)
            doc.is_set = False
            doc.default = None
            doc.is_entity = False

    return all_ent_docs


def code_from_db_and_docs(ent: db.Entity) -> tuple[
    dict[str, AllInfoStr],
    dict[str, Dict[List[str], List[str]]]]:
    """
    Объединяет информацию о сущности из кода сущности и документации
    :param ent:
    :return:
    """
    all_ent_code, p_k, *_ = db_ent_to_dict(ent)
    all_ent_docs: dict[str, DbDocs] = info_from_docs(ent)

    if "password" in all_ent_code:
        print("code", all_ent_code["password"].dict().items(), " ", sep='\n')
    if "password" in all_ent_docs:
        print("docs", all_ent_docs["password"].dict().items(), " ", sep='\n')

    _all_ent_docs: dict[str, AllInfoStr] = {
        name: AllInfoStr(**(
                (all_ent_docs[name].dict(exclude_unset=True, exclude_none=True, exclude_defaults=True)
                 if all_ent_docs.get(name) else dict()) |
                (all_ent_code[name].dict(exclude_unset=True, exclude_none=True, exclude_defaults=True)
                 if all_ent_code.get(name) else dict()) |
                {"class_name": ent.__name__}
        ))
        for name in (all_ent_docs | all_ent_code).keys()}
    if "password" in all_ent_code or  "password" in all_ent_docs:
        print("all_code", _all_ent_docs["password"].dict().items(), " ", sep='\n')
    return _all_ent_docs, p_k


if __name__ == "__main__":
    create_db_models()
