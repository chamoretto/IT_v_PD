from typing import Tuple, Dict, List, Union, Optional, Any
from functools import reduce

from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.db.raw_models import db


class StringDB(BaseModel):
    """Олицетворяет одну строку в классе сузности Pony"""

    name: str  # имя поля (атрибута)
    db_type: str  # Set, Optional, Requires, PrimaryKey
    param_type: str  # тип параметра, записываемого в БД
    default: Any = None  # параметр по умолчанию
    other_params: dict  # другие параметры
    is_primary_key: bool = False  #


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


def db_ent_to_dict(ent) -> Tuple[
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
    for name, ent in db.entities.items():
        ent.describe()


