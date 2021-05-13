from typing import Optional, Dict, Any, Callable
from collections import defaultdict
import enum

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


def default_html(param: DbDocs) -> str:
    # language=HTML
    text = f'<div class="margin-bottom-sm">' \
           f'<label class="form-label margin-bottom-xxs">\n' \
           f'{param.name} имеет тип {param.html_type}, который еще не поддерживается...\n' \
           f'</label></div>\n' \

    return text


def html_text(param: DbDocs) -> str:
    # l anguage=HTML
    value = f'''
        {'{{'}
                ('value="' + {param.class_name.lower()}.{param.name} + '"'
                if {param.class_name.lower()} is defined
                else
                {"'" + 'value="' + str(param.default) + '"' + "'|safe" if param.default is not None and bool(param.default) else '""'})|safe
        {'}}'}'''
    text = f'{"{%"} if ({param.class_name.lower()} is defined and {param.class_name.lower()}.{param.name} != Undefined) or {param.class_name.lower()} is not defined {"%}"}'
    text += f'<div class="margin-bottom-sm">\n' \
           f'<label class="form-label margin-bottom-xxs" for="{param.class_name}_{param.name}">{param.name}\n' \
           f'{"""<span class="color-error">*</span>""" if param.required else ""}</label>\n' \
           f'<input class="form-control width-100% text-sm" placeholder="{param.placeholder}"' \
           f' type="text" name="{param.name}" id="{param.class_name}_{param.name}"' \
           f' {value}' \
           f'{" required" if param.required else ""} {"{{"} ("disabled" if disabled is defined and disabled else "")|safe {"}}"}>\n' \
           f'<div id="{param.class_name}_{param.name}_error"></div></div>'
    text += '{% endif %}'
    return text


def html_password(param: DbDocs) -> str:
    return ""


def html_select(param: DbDocs) -> str:
    # language=HTML
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
    FieldHtmlType.SELECT: html_select
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

    with open(join(HOME_DIR, "content", "templates", "database", f"{ent.__name__}_form.html"), "w", encoding='utf-8') as f:
        print(html_form, file=f)


if __name__ == '__main__':
    create_pd_models()
    for name, ent in m.db.entities.items():
        print(name)
        create_html_file(ent)
    # print(type(FieldHtmlType.get_obj("text")))



