from typing import Optional, Dict, Any, Callable, Union
from collections import defaultdict
import enum
from itertools import chain

from app.db import models as m
from app.pydantic_models import db_models as pd
from app.db._change_db._create_models import db_ent_to_dict
from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.pydantic_models.create_pydantic_models import create_pd_models
from app.settings.config import HOME_DIR, join


@enum.unique
class AccessType(enum.Enum):
    PUBLIC = "public"
    USER = "user"
    SMMER = "smm"
    DIRECTION_EXPERT = "expert"
    ADMIN = "admin"
    DEVELOPER = "dev"

    @classmethod
    def get_obj(cls, val: str):
        if val in cls._value2member_map_:
            return cls._value2member_map_[val]
        print(val)
        raise AttributeError

    def __str__(self):
        return self.value


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

    def __str__(self):
        return self.value

    @classmethod
    def get_obj(cls, val: str):
        if val in cls._value2member_map_:
            return cls._value2member_map_[val]
        print(val)
        raise AttributeError


class DbDocs(BaseModel):
    name: str
    description: Optional[str]
    html_type: Optional[FieldHtmlType]
    access: list[AccessType] = [AccessType.DEVELOPER]
    required: bool = False
    class_name: str
    placeholder: str = ""
    default: str = None
    is_entity: bool = False
    is_set: bool = False


def all_html_form(content: str, entity_name: str) -> str:
    # langua ge=HTML
    text = f'<div class="container max-width-lg">\n' \
           f'{"{%"} if disabled is not defined or not disabled {"%}"}' \
           f'<form id="{{entity_name.lower()}}"' \
           f' action="{"{{"}(action_url if action_url is defined else "/db/{entity_name}/new")|safe {"}}"}"' \
           f' method="{"{{"} (send_method if send_method is defined else "post")|safe {"}}"}"' \
           f' enctype="multipart/form-data" onsubmit="return false">\n' \
           f'{"{%"} endif {"%}"}' \
           f'<fieldset class="margin-bottom-md">\n' \
           f'<legend class="form-legend">{entity_name}</legend>\n' \
           f'{content}' \
           f'</fieldset>' \
           f'{"{%"} if disabled is not defined or not disabled {"%}"}' \
           f'<div>\n' \
           f'<button class="btn btn--primary" type="submit" id="submit">Отправить</button>\n' \
           f'<button class="btn btn--subtle" type="reset">Сбросить</button>\n' \
           f'</div></form>' \
           f'{"{%"} endif {"%}"}' \
           f'</div>' \
           f'<script src="{"{{"}url_for("scripts", path="/async_forms_and_redirects.js"){"}}"}"></script>'
    return text


def field_decorator(func: Callable) -> Callable:
    def _decorator(param: DbDocs, *args, **kwargs) -> str:
        text = f'{"{%"} if ({param.class_name.lower()} is defined and' \
               f' {param.class_name.lower()}.{param.name} != Undefined)' \
               f' or {param.class_name.lower()} is not defined {"%}"}'
        text += func(param, *args, **kwargs)
        text += f'<div id="{param.class_name}_{param.name}_error"></div>'
        text += '{% endif %}'
        return text

    return _decorator


def default_html(param: DbDocs) -> str:
    # la nguage=HTML
    text = f'<div class="margin-bottom-sm">' \
           f'<label class="form-label margin-bottom-xxs">\n' \
           f'{param.name} имеет тип {param.html_type}, который еще не поддерживается...\n' \
           f'</label></div>\n'

    return text


def _get_name(param: DbDocs) -> str:
    return f'name="{param.name}"'


def _get_raw_id(param: DbDocs) -> str:
    return f'{param.class_name}_{param.name}'


def _get_id(param: DbDocs) -> str:
    return f'id="{_get_raw_id(param)}'


def _get_placeholder(param: DbDocs) -> str:
    return f'placeholder="{param.placeholder}"'


def _required_field(param: DbDocs) -> str:
    return f'{" required" if param.required else ""}'


def _disabled_field(param: DbDocs) -> str:
    return f'{"{{"} ("disabled" if disabled is defined and disabled else "")|safe {"}}"}'


def _get_value_code(param: DbDocs) -> str:
    return f'''{'{{'}('value="' + {param.class_name.lower()}.{param.name} + '"'
        if {param.class_name.lower()} is defined
        else {(("'" + 'value="' + str(param.default) + '"' + "'|safe") if (
            param.default is not None and bool(param.default)) else '""')})|safe {'}}'}'''


def get_text_label(param: DbDocs, l_class="form-label margin-bottom-xxs") -> str:
    return f'<label class="{l_class}" for="{_get_raw_id(param)}">{param.name}\n' \
           f'{"""<span class="color-error">*</span>""" if param.required else ""}</label>\n'


def required_options_into_input(param: DbDocs) -> str:
    _data = [
        _get_name,
        _get_id,
        _get_placeholder,
        _get_value_code,
        _required_field,
        _disabled_field
    ]
    return " ".join([i(param) for i in _data])


@field_decorator
def html_text(param: DbDocs) -> str:
    # la nguage=HTML

    text = f'<div class="margin-bottom-sm">\n' \
           f'{get_text_label(param)}' \
           f'<input class="form-control width-100% text-sm"' \
           f' type="text" {required_options_into_input(param)}>\n' \
           f'</div>'
    return text


@field_decorator
def html_password(param: DbDocs) -> str:
    text = f'<div class="margin-bottom-sm">' \
           f'<div class="flex justify-between margin-bottom-xxxs">' \
           f'{get_text_label(param)}' \
           f'</div><div class="password js-password">' \
           f'<input class="form-control width-100% password__input js-password__input"' \
           f' type="password" {required_options_into_input(param)} >' \
           f'<button class="password__btn flex flex-center js-password__btn" aria-hidden="true">' \
           f'<span class="password__btn-label" title="Show Password">' \
           f'<svg class="icon block" viewBox="0 0 32 32">' \
           f'<g stroke-linecap="square" stroke-linejoin="miter" stroke-width="2"' \
           f' stroke="currentColor" fill="none">' \
           f'<path d="M1.409,17.182a1.936,1.936,0,0,1-.008-2.37C3.422,12.162,8.886,6,16,6c7.02,0,12.536,6.158,' \
           f'14.585,8.81a1.937,1.937,0,0,1,0,2.38C28.536,19.842,23.02,26,16,26S3.453,19.828,1.409,17.182Z"' \
           f' stroke-miterlimit="10"></path><circle cx="16" cy="16" r="6" stroke-miterlimit="10">' \
           f'</circle></g></svg></span>' \
           f'<span class="password__btn-label" title="Hide Password">' \
           f'<svg class="icon block" viewBox="0 0 32 32">' \
           f'<g stroke-linecap="square" stroke-linejoin="miter" stroke-width="2" stroke="currentColor" ' \
           f'fill="none"><path data-cap="butt" ' \
           f'd="M8.373,23.627a27.659,27.659,0,0,1-6.958-6.445,1.938,1.938,0,0,1-.008-2.37C3.428,12.162,8.892,' \
           f'6,16.006,6a14.545,14.545,0,0,1,7.626,2.368"' \
           f' stroke-miterlimit="10" stroke-linecap="butt">' \
           f'</path><path d="M27,10.923a30.256,30.256,0,0,1,3.591,3.887,1.937,1.937,0,0,1,0,2.38C28.542,19.842,23.026,' \
           f'26,16.006,26A12.843,12.843,0,0,1,12,25.341" ' \
           f'stroke-miterlimit="10"></path><path data-cap="butt"' \
           f' d="M11.764,20.243a6,6,0,0,1,8.482-8.489" stroke-miterlimit="10" stroke-linecap="butt">' \
           f'</path><path d="M21.923,15a6.005,6.005,0,0,1-5.917,7A6.061,6.061,0,0,1,15,21.916"' \
           f' stroke-miterlimit="10"></path>' \
           f'<line x1="2" y1="30" x2="30" y2="2" fill="none" stroke-miterlimit="10"></line></g></svg>' \
           f'</span></button> </div></div>' \
           f'</div>'
    return text


def _base_html_file(
        param: DbDocs,
        multiple: bool = False,  # разрешить множественный выбор?
        file_type: Union[str, list[str], None] = None,
        file_filter=lambda f: True  # Фильтр, который оставляет только нужные типы файлов
) -> str:

    from app.settings.mime_types import mime_types

    _dict: dict[str, list[str]] = {
        "img": ["image"],
        "document": ["doc", "msword", "dot", "zip", "pdf"]
    }
    file_type = file_type or ['all']
    if type(file_type) == str:
        file_type = [file_type]
    groups = frozenset(chain(*(_dict.get(i, ["all"]) for i in file_type)))

    return f'<fieldset class="file-upload margin-bottom-sm">' \
           f'{get_text_label(param)}<br>' \
           f'<label for="{_get_raw_id(param)}" class="file-upload__label btn btn--primary">' \
           f'<span class="flex items-center">' \
           f'<span class="file-upload__text">{{obj.get(id) or _type.TEXT}}</span>' \
           f'</span> </label> ' \
           f'<input type="file" accept=' \
           f'"{ ",".join(file_type for type_group in (mime_types[key] for key in groups if mime_types.get(key))  for file_type in filter(file_filter, type_group))}" ' \
           f'class="file-upload__input" {required_options_into_input(param)} {" multiple" if multiple else ""}>' \
           f'</fieldset>'


@field_decorator
def html_image(param: DbDocs):
    return _base_html_file(param, file_type='img')


@field_decorator
def html_text_file(param: DbDocs):
    return _base_html_file(param, file_type='document')


@field_decorator
def html_select(param: DbDocs) -> str:
    # langu age=HTML
    text = f'<label class="form-label margin-bottom-xxxs" for="{param.class_name}_{param.name}">{param.name} ' \
           f'{"""<span class="color-error">*</span>""" if param.required else ""}</label>' \
           f'<div class="select">' \
           f'<select class="select__input form-control text-sm"' \
           f' name="{param.name}" id="{param.class_name}_{param.name}"' \
           f'{" multiple" if param.is_set else ""}' \
           f'{" required" if param.required else ""}' \
           f'<option disabled {{"" if {param.class_name.lower()} is defined ' \
           f' and bool({param.class_name.lower()}.{param.name}) else "selected"}}>{param.placeholder}</option>'
    return text


def get_doc(ent):
    if ent.__doc__:
        return ent.__doc__ + "\n".join(
            [get_doc(parent) for parent in ent.__bases__ if parent.__name__ in m.db.entities])
    return ""


type_to_html: dict[FieldHtmlType, Callable[[DbDocs], str]] = defaultdict(lambda: default_html)
type_to_html.update({
    FieldHtmlType.TEXT: html_text,
    FieldHtmlType.SELECT: html_select,
    FieldHtmlType.PASSWORD: html_password,
    FieldHtmlType.IMAGE: html_image,
    FieldHtmlType.FILE: html_text_file
})


def create_html_file(ent: m.db.Entity):
    keys_convertor: dict[str, str] = {
        "type": "html_type",
        "param": "description"
    }
    vals_convertor: dict[str, Callable] = defaultdict(
        lambda: str,
        type=FieldHtmlType.get_obj,
        mod=AccessType.get_obj
    )

    good_start: list[str] = [":param", ":type", ":mod"]

    pd_ent = getattr(pd, ent.__name__)
    # print(pd_ent)
    all_ent_docs: dict[str, DbDocs] = defaultdict(lambda: DbDocs(name=n.strip(), class_name=ent.__name__))

    all_docs = [i.strip() for i in get_doc(ent).split("\n")]
    # print(*all_docs, sep="\n")
    all_docs = (i[1:].split(":") for i in all_docs if bool(i) and any(i.startswith(j) for j in good_start))
    all_docs = (t.split() + [d.strip()] for [t, d] in all_docs)

    code, pk = db_ent_to_dict(ent)

    for [t, n, d] in all_docs:
        obj: DbDocs = all_ent_docs[n.strip()]
        all_ent_docs[n.strip()] = DbDocs(**(obj.dict(exclude_unset=True) |
                                            {keys_convertor[t]: vals_convertor[t](d)}))

    for name, doc in all_ent_docs.items():
        if code.get(name):
            doc.required = code[name].db_type in ["PrimaryKey", "Required"]
            doc.is_set = not doc.required and code[name].db_type in ["Set"]
            doc.default = getattr(pd_ent.__fields__[name], "default")
            # print(ent.__name__, name, doc.default)
            doc.is_entity = any(i in code[name].param_type for i in m.db.entities)
        else:
            doc.required = code.get(name, True)
            doc.is_set = False
            doc.default = None
            doc.is_entity = False

    html_form = [type_to_html[val.html_type](val) for key, val in all_ent_docs.items()]
    html_form = all_html_form("\n".join(html_form), ent.__name__)
    html_form = "{# =======!!! ВНИМАНИЕ !!!======= #}\n" \
                "{# =======! Этот файл генерируется автоматически" \
                " на основе документации класса сущности БД в файле app/db/models.py !=======#}\n\n" \
                "{# =======! Ни одно изменение в этом файле не будет сохранено! !======= #}\n\n" + html_form

    with open(join(HOME_DIR, "content", "templates", "database", f"{ent.__name__}_form.html"), "w",
              encoding='utf-8') as f:
        print(html_form, file=f)


if __name__ == '__main__':
    create_pd_models()
    for name, ent in m.db.entities.items():
        print(name)
        create_html_file(ent)
    # print(type(FieldHtmlType.get_obj("text")))
