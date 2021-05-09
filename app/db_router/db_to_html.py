from typing import Optional, Dict, Any, Callable
from collections import defaultdict
from fast_enum import FastEnum

from app.db import models as m
from app.pydantic_models import db_models as pd
from app.db._change_db._create_models import db_ent_to_dict
from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.pydantic_models.create_pydantic_models import create_pd_models
from app.settings.config import HOME_DIR, join


# class HtmlInputTemplates(metaclass=FastEnum):
#    text = '<div class="margin-bottom-sm">' \
#           '<label class="form-label margin-bottom-xxs" for="{{id}}">' \
#           '{{"<span class="color-error">*</span>"|safe if required else ""}}</label>'
#    B = 2


class DbDocs(BaseModel):
    name: str
    description: Optional[str]
    html_type: Optional[str]
    required: bool = False
    class_name: str
    placeholder: str = ""
    default: str = None
    is_entity: bool = False
    is_set: bool = False


def all_html_form(content: str, entity_name: str) -> str:
    # langua ge=HTML
    text = f'<div class="container max-width-lg">\n' \
           f'<form id="{{entity_name.lower()}}" action="/db/{entity_name}/new" method="post"' \
           f' enctype="multipart/form-data" onsubmit="return false">\n' \
           f'<fieldset class="margin-bottom-md">\n' \
           f'<legend class="form-legend">{entity_name}</legend>\n' \
           f'{content}' \
           f'</fieldset><div>\n' \
           f'<button class="btn btn--primary" type="submit" id="submit">Отправить</button>\n' \
           f'<button class="btn btn--subtle" type="reset">Сбросить</button>\n' \
           f'</div></form></div>' \
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
                'value="' + {param.class_name.lower()}.{param.name} + '"'
                if {param.class_name.lower()} is defined
                else
                {"'" + 'value="' + str(param.default) + '"' + "'|safe" if param.default is not None and bool(param.default) else '""'}
        {'}}'}'''
    text = f'<div class="margin-bottom-sm">\n' \
           f'<label class="form-label margin-bottom-xxs" for="{param.class_name}_{param.name}">{param.name}\n' \
           f'{"""<span class="color-error">*</span>""" if param.required else ""}</label>\n' \
           f'<input class="form-control width-100% text-sm" placeholder="{param.placeholder}"' \
           f' type="text" name="{param.name}" id="{param.class_name}_{param.name}"' \
           f' {value}' \
           f'{" required" if param.required else ""}>\n' \
           f'<div id="{param.class_name}_{param.name}_error"></div></div>'
    return text


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


type_to_html: dict[str, Callable[[DbDocs], str]] = defaultdict(
    lambda: default_html,
    text=html_text,
    no_supported_select=html_select
)


def create_html_file(ent: m.db.Entity):
    pd_ent = getattr(pd, ent.__name__)
    all_ent_docs: Dict[str, DbDocs] = {}
    all_docs = (i.strip() for i in get_doc(ent).split("\n"))
    all_docs = (i[1:].split(":") for i in all_docs if bool(i) and (i.startswith(":param") or i.startswith(":type")))
    all_docs = (t.split() + [d.strip()] for [t, d] in all_docs)
    code, pk = db_ent_to_dict(ent)
    for [t, n, d] in all_docs:
        obj = all_ent_docs.get(n.strip(), DbDocs(name=n.strip(), class_name=ent.__name__))
        setattr(obj, ("html_type" if t.strip() == "type" else "description"), d)
        all_ent_docs[n.strip()] = obj
    for name, doc in all_ent_docs.items():
        doc.required = code[name].db_type in ["PrimaryKey", "Required"]
        doc.is_set = code[name].db_type in ["Set"]
        doc.default = getattr(pd_ent.__fields__[name], "default")
        print(ent.__name__, name, doc.default)
        doc.is_entity = any(i in code[name].param_type for i in m.db.entities)

    # print(*all_ent_docs.items(), sep="\n")
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
        create_html_file(ent)

