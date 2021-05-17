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
    SELF = "self"

    @classmethod
    def get_obj(cls, val: str):
        if val in cls._value2member_map_:
            return cls._value2member_map_[val]
        print(val)
        raise AttributeError

    def __str__(self):
        return self.value


@enum.unique
class AccessMode(enum.Enum):
    CREATE = "create"
    EDIT = "edit"
    LOOK = "look"

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


class DbDocs(BaseModel):
    name: str
    description: Optional[str]
    html_type: Optional[FieldHtmlType]
    access: dict[AccessType, list[AccessMode]] = dict()
    required: bool = False
    class_name: str
    placeholder: str = ""
    default: str = None
    is_entity: bool = False
    is_set: bool = False


def all_html_form(content: str, entity_name: str) -> str:
    # langua ge=HTML
    text = f'' \
           f'<div class="container max-width-lg">\n' \
           f'<h3 class="margin-bottom-sm">' \
           f'<a href="/db/{entity_name}" class="no-effect" title="Вернуться к просмотру объектов БД">' \
           f'<i class="fa fa-long-arrow-alt-left"></i></a>' \
           f'Вернуться ко всем объектам {entity_name}</h3>' \
           f'{"{%"} if (disabled is not defined or not disabled) or' \
           f' (access_mode is defined and access_mode != "look") {"%}"}\n' \
           f'{"{#{"}access_mode{"}#}"}\n' \
           f'<form id="{entity_name.lower()}"' \
           f' action="{"{{"}(action_url if action_url is defined else "/db/{entity_name}/new")|safe {"}}"}"' \
           f' method="{"{{"} (send_method if send_method is defined else "post")|safe {"}}"}"' \
           f' enctype="multipart/form-data" onsubmit="return false">\n' \
           f'{"{%"} endif {"%}"}\n' \
           f'<fieldset class="margin-bottom-md">\n' \
           f'<legend class="form-legend">{entity_name}</legend>\n' \
           f'{content}' \
           f'</fieldset>' \
           f'{"{%"} if (disabled is not defined or not disabled) or' \
           f' (access_mode is defined and access_mode != "look")  {"%}"}' \
           f'<div>\n' \
           f'<button class="btn btn--primary" type="submit" id="submit">Отправить</button>\n' \
           f'<button class="btn btn--subtle" type="reset">Сбросить</button>\n' \
           f'</div></form>\n' \
           f'{"{%"} endif {"%}"}\n' \
           f'</div>' \
           f'<script src="{"{{"}url_for("scripts", path="/async_forms_and_redirects.js"){"}}"}"></script>'
    return text


def field_decorator(func: Callable) -> Callable:
    def _decorator(param: DbDocs, *args, **kwargs) -> str:
        text = f'' \
               f'{"{%"} if access_mode is defined and access is defined {"%}"}\n' \
               f'   {"{%"} set ns = namespace(good_modes=[]) {"%}"}\n' \
               f'   {"{%"} set access_dict = {str({str(key): [str(i) for i in val] for key, val in param.access.items()})} {"%}"}\n' \
               f'   {"{%"} for a in access {"%}"}\n' \
               f'       {"{%"} set ns.good_modes = ns.good_modes + access_dict.get(a, []) {"%}"}\n' \
               '    {% endfor %}\n' \
               f'   {"{%"} if access_mode in ns.good_modes {"%}"}\n'
        text += f'      {"{%"} if ({param.class_name.lower()} is defined and' \
               f' {param.class_name.lower()}.{param.name} != Undefined)' \
               f' or {param.class_name.lower()} is not defined {"%}"}\n'
        text += func(param, *args, **kwargs)
        text += f'<div id="{param.class_name}_{param.name}_error"></div>'
        text += '{% endif %}{% endif %}{% endif %}'
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
    return f'id="{_get_raw_id(param)}"'


def _get_placeholder(param: DbDocs) -> str:
    return f'placeholder="{param.placeholder}"'


def _required_field(param: DbDocs) -> str:
    return f'{" required" if param.required else ""}'


def _disabled_field(param: DbDocs) -> str:
    return f'{"{{"} ("disabled" if (disabled is defined and disabled) or ' \
           f'(access_mode is defined and access_mode == "look")  else "")|safe {"}}"}'


def _get_value_code(param: DbDocs) -> str:
    return f'''{'{{'}
    ('value="%s"' % ({param.class_name.lower()}.{param.name} if {param.class_name.lower()}.{param.name} else "")
        if {param.class_name.lower()} is defined
        else {(("'" + 'value="' + str(param.default) + '"' + "'|safe") if (
            param.default is not None and bool(param.default)) else '""')})|safe {'}}'}'''


def _get_checkbox_value(param: DbDocs) -> str:
    return f'''{"{{"} (( "checked" if {param.class_name.lower()}.{param.name} else "" )|safe 
    if {param.class_name.lower()} is defined else
            {'"checked"' if param.default is not None and param.default else '""'}|safe ){'}}'}'''


def get_text_label(param: DbDocs, l_class="form-label margin-bottom-xxs") -> str:
    return f'<label class="{l_class}" for="{_get_raw_id(param)}">{param.description}\n' \
           f'{"""<span class="color-error">*</span>""" if param.required else ""}</label>\n'


def required_options_into_input(param: DbDocs, black_list=[]) -> str:
    _data = [
        _get_name,
        _get_id,
        _get_placeholder,
        _get_value_code,
        _required_field,
        _disabled_field
    ]
    return " ".join([i(param) for i in _data if i not in black_list])


@field_decorator
def html_text(param: DbDocs, html_input_type="text") -> str:
    # la nguage=HTML

    text = f'<div class="margin-bottom-sm">\n' \
           f'{get_text_label(param)}' \
           f'<input class="form-control width-100% text-sm"' \
           f' type="{html_input_type}" {required_options_into_input(param)}>\n' \
           f'</div>'
    return text

def html_number(param: DbDocs)-> str:
    return html_text(param, html_input_type='number')


@field_decorator
def html_password(param: DbDocs) -> str:
    # language=HTML
    text = f'<div class="margin-bottom-sm">' \
           f'<div class="flex justify-between margin-bottom-xxxs">' \
           f'{get_text_label(param)}' \
           f'</div>' \
           f'<div class="password js-password">' \
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
           f'</span></button>' \
           f'</div>' \
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
           f'<span class="file-upload__text" id="{_get_raw_id(param)}_span">' \
           f'{"{% set value = " + _get_value_code(param).replace("{{", "").replace("}}", "") + " %}"}' \
           f'{"{{"} value | replace("value=", "") | replace(\'"\', "")' \
           f' if "value" in value and value | replace("value=", "") | replace(\'"\', "") != \'""\' ' \
           f'else "Загрузить" {"}}"}</span>' \
           f'</span> </label> ' \
           f'<input type="file" accept=' \
           f'"{",".join(file_type for type_group in (mime_types[key] for key in groups if mime_types.get(key)) for file_type in filter(file_filter, type_group))}" ' \
           f'class="file-upload__input"  {required_options_into_input(param)} {" multiple" if multiple else ""} {_get_value_code(param)} tabindex="-1">' \
           f'</fieldset>'


@field_decorator
def html_image(param: DbDocs):
    return _base_html_file(param, file_type='img')


@field_decorator
def html_text_file(param: DbDocs):
    return _base_html_file(param, file_type='document')


def html_bool(param: DbDocs):
    text = f"""<div class="col-6@md">
                        <fieldset class="margin-bottom-md">
                            <h4 class="text-start margin-bottom-sm"> {param.description} </h4>
                            <div class="margin-bottom-sm" style="display: flex;">
                                <div class="switch margin-left-sm">
                                    <input class="switch__input" type="checkbox"
                                    {required_options_into_input(param, black_list=[_get_value_code])}
                                    {_get_checkbox_value(param)}>
                                    <label aria-hidden="true" class="switch__label" for="{_get_raw_id(param)}">{param.name}</label>
                                    <div aria-hidden="true" class="switch__marker"></div>
                                </div>
                            </div>
                        </fieldset>
                    </div>"""
    # text = f""" <fieldset class="margin-bottom-md"> <input type="checkbox" {required_options_into_input(param, black_list=[_get_value_code])} value="true" ></fieldset>"""
    return text


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


@field_decorator
def datetime_html(param: DbDocs, html_input_type="datetime-local") -> str:
    return f'<fieldset class="margin-bottom-md">\n' \
           f'<div class="margin-bottom-sm">\n' \
           f'<label class="form-label margin-bottom-xxs" for="date_start">{param.description}</label>\n' \
           f'<input class="form-control width-100% text-sm"' \
           f' type="{html_input_type}" {required_options_into_input(param, black_list=[_get_value_code])}\n' \
           f'{"{% set value = " + _get_value_code(param).replace("{{", "").replace("}}", "") + " %}"}\n' \
           f'{"{%"} if "value" in value and value.split()|length == 2 {"%}"}\n' \
           f'{"{{"}value.split() | join("T"){"}}"}\n' \
           f'{"{%"} else {"%}"}\n' \
           f'{"{{"}value{"}}"}\n' \
           f'{"{%"} endif {"%}"}\n' \
           f'>\n' \
           f'</div></fieldset>\n'


def date_html(param: DbDocs) -> str:
    return datetime_html(param, html_input_type='date')


def time_html(param: DbDocs) -> str:
    return datetime_html(param, html_input_type='time')


def get_doc(ent):
    if ent.__doc__:
        return "\n".join(
            [get_doc(parent) for parent in ent.__bases__ if parent.__name__ in m.db.entities]) + "\n" + ent.__doc__
    return ""


type_to_html: dict[FieldHtmlType, Callable[[DbDocs], str]] = defaultdict(lambda: default_html)
type_to_html.update({
    FieldHtmlType.TEXT: html_text,
    # FieldHtmlType.SELECT: html_select,
    FieldHtmlType.PASSWORD: html_password,
    FieldHtmlType.IMAGE: html_image,
    FieldHtmlType.FILE: html_text_file,
    FieldHtmlType.BOOL: html_bool,
    FieldHtmlType.NUMBER: html_number,
    FieldHtmlType.DATE: date_html,
    FieldHtmlType.TIME: time_html,
    FieldHtmlType.DATETIME: datetime_html,
})


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


def create_html_file(ent: m.db.Entity):
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
    all_docs = [i[1:].split(":") for i in all_docs if not print(i) and bool(i) and not print(i) and any(i.strip().startswith(j) or i.strip().startswith(":mod") or i.strip().startswith(":access") for j in good_start) and not print(i)]
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
        # print(name)
        create_html_file(ent)
    # print(type(FieldHtmlType.get_obj("text")))
