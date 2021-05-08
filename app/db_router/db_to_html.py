from typing import Optional, Dict

from fast_enum import FastEnum

from app.db import models as m
from app.pydantic_models import db_models as pd
from app.pydantic_models.standart_methhods_redefinition import BaseModel


class HtmlInputTemplates(metaclass=FastEnum):
   text = '<div class="margin-bottom-sm">' \
          '<label class="form-label margin-bottom-xxs" for="{{id}}">' \
          '{{"<span class="color-error">*</span>"|safe if required else ""}}</label>'
   B = 2


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


def html_text(param: DbDocs):
    # language=HTML
    text = f'<div class="margin-bottom-sm">' \
           f'<label class="form-label margin-bottom-xxs" for="{param.class_name}_{param.name}">{param.name}' \
           f'{"""<span class="color-error">*</span>""" if param.required else ""}</label>' \
           f'<input class="form-control width-100% text-sm" placeholder="{param.placeholder}"' \
           f' type="text" name="{param.name}" id="{param.class_name}_{param.name}"' \
           f' {{ value="{param.class_name.lower()}.{param.name}" if {param.class_name.lower()} is defined' \
           f' else {param.default if param.default is not None else ""} }}' \
           f'{" required" if param.required else ""}></div>'
    return text


def html_select(param: DbDocs):
    # language=HTML
    text = f'<label class="form-label margin-bottom-xxxs" for="{param.class_name}_{param.name}">{param.name} ' \
           f'{"""<span class="color-error">*</span>""" if param.required else ""}</label>' \
           f'<div class="select">' \
           f'<select class="select__input form-control text-sm"' \
           f' name="{param.name}" id="{param.class_name}_{param.name}"' \
           f'{" multiple" if param.is_set else ""}' \
           f'{" required" if param.required else ""}' \
           f'<option disabled {{"" if {param.class_name.lower()} is defined ' \
           f' and bool({param.class_name.lower()}.{param.name}) else "selected"}}>{param.placeholder}</option>' \
           f''


def get_doc(ent):
    if ent.__doc__:
        return ent.__doc__ + "\n".join(
            [get_doc(parent) for parent in ent.__bases__ if parent.__name__ in m.db.entities])
    return ""


def create_html_file(ent, pd_ent):
    all_ent_docs: Dict[str, DbDocs] = {}
    all_docs = (i.strip() for i in get_doc(ent).split("\n"))
    all_docs = (i[1:].split(":") for i in all_docs if bool(i) and (i.startswith(":param") or i.startswith(":type")))
    all_docs = (t.split() + [d.strip()] for [t, d] in all_docs)
    for [t, n, d] in all_docs:
        obj = all_ent_docs.get(n.strip(), DbDocs(name=n.strip(), class_name=ent.__name__))
        setattr(obj, ("html_type" if t.strip() == "type" else "description"), d)
        all_ent_docs[n.strip()] = obj

    print(*all_ent_docs.items(), sep='\n')


create_html_file(m.User, None)

