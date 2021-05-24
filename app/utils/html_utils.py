from __future__ import annotations
from functools import reduce, wraps

from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.pydantic_models.standart_methhods_redefinition import BaseModel


class Alert:
    # PRIMARY = "primary"
    # SECONDARY = "secondary"
    SUCCESS = "success"
    # DANGER = "danger"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

    # LIGHT = "light"
    # DARK = "dark"

    def __init__(self, content: str, alert_type=SUCCESS):
        self.content = content
        self.alert_type = alert_type

    @property
    def conv(self):
        return {
            "content": self.content,
            "type": self.alert_type
        }

    def alert_renderer(self, request: Request = None, basic_data: dict = dict) -> str:
        """ Переопределён ниже """
        return str(self)

    def __dir__(self):
        return self.conv

    def __str__(self):
        return 'Alert(%s): "%s"' % (self.alert_type.capitalize(), self.content)

    def __repr__(self):
        return "<Alert(%s) %.10s>" % (self.alert_type.capitalize(), self.content)


class SitePageMenu(BaseModel):
    name: str
    href: str = "/novator"


def get_nice_table(data):
    change_table = {
        "<table>": '<table class="max-width-lg margin-x-auto table js-table table--expanded@sm width-100% margin-bottom-md table--expanded table--loaded">',
        "<thead>": '<thead class="table__header table__header--sticky">',
        "<tr>": '<tr class="table__row">',
        '<th>': '<th class="table__cell text-left" scope="col">',
        "<tbody>": '<tbody  class="table__body">',
        "<td>": ' <td class="table__cell text-center" role="cell">',
    }
    data = reduce(lambda string, i: string.replace(i[0], i[1]), change_table.items(), data)
    return data


def get_nice_table_page(table, href="*"):
    text = f'<div class="container max-width-adaptive-lg">' \
           f'<h3 class="margin-bottom-sm">' \
           f'  <a href="/db" class="no-effect url_as_ajax" title="Вернуться к базе данных">' \
           f'<i class="fa fa-long-arrow-alt-left"></i></a></h3><h4>' \
           f'<a href="/db" class="url_as_ajax">Перейти а главную страницу БД</a></h4><br>'
    text += get_nice_table(table)
    text += '<div class="margin-bottom-lg' \
            ' {{\'text-right\' if useless_human_from_old_project is defined else \'inline-block\'}}">' \
            f'<a href="{href}" class="btn btn--primary url_as_ajax"><i class="far fa-compass"></i>' \
            f' Добавить объект в БД</a></div></div>'
    return text


def nice_table_page(func):
    @wraps(func)
    def decorator(cls, *a, **k):
        return get_nice_table_page(func(cls, *a, **k), href=f'/db/{cls.__name__}/new')

    return decorator


_public_template = Jinja2Templates("content/templates/public_temp")
_layout_env = Jinja2Templates("content/templates/layout")
_skeleton_template = _layout_env.get_template("skeleton.html")
_alert_template = _layout_env.get_template("alert.html")
_admin_shell_template = _layout_env.get_template("admin_shell.html")


def alert_renderer(alert: Alert, request: Request = None, basic_data: dict = dict()) -> str:
    if "request" not in basic_data:
        basic_data['request'] = request
    if basic_data['request']:
        return _alert_template.render(basic_data | {"alert": alert})
    raise AttributeError


def shell_renderer(shell: dict[str, 'PdUrl'], request: Request = None, basic_data: dict = dict()) -> str:
    if "request" not in basic_data:
        basic_data['request'] = request
    if basic_data['request']:
        return _admin_shell_template.render(basic_data | {"pages": shell})
    raise AttributeError


Alert.alert_renderer = alert_renderer


