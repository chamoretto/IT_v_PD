import typing
from typing import Union, Optional, Any, Type

try:
    import jinja2
except ImportError:  # pragma: nocover
    jinja2 = None  # type: ignore

from starlette.background import BackgroundTask
from starlette.responses import Response
from starlette.types import Receive, Scope, Send
from fastapi.responses import JSONResponse, RedirectResponse
from pony.orm import db_session
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.utils.html_utils import SitePageMenu
from app.pydantic_models.response_models import code_to_resp, PdUrl
from app.pydantic_models import simple_entities as easy_ent_pd
from app.pydantic_models.gen import output_ent as out_pd
from app.db import models as m
from app.pydantic_models.standart_methhods_redefinition import AccessType, AccessMode
from app.utils.html_utils import _public_template, _skeleton_template, _alert_template, _admin_shell_template
from app.utils.responses import RedirectResponseWithBody
from app.pydantic_models.response_models import Ajax200Answer, BaseHTMLDataResponse, GenResp


class _MyTemplateResponse(Response):
    media_type = "text/html"

    def __init__(
            self,
            template: typing.Any,
            context: dict,
            status_code: int = 200,
            headers: dict = None,
            media_type: str = None,
            background: BackgroundTask = None,

    ):
        self.template = template
        self.context = context
        self.jinja2_template = True
        content = template.render(context)
        # content = "<p>Тут должна быть страница, но ее нет</p>"
        super().__init__(content, status_code, headers, media_type, background)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        request = self.context.get("request", {})
        extensions = request.get("extensions", {})
        if "http.response.template" in extensions:
            await send(
                {
                    "type": "http.response.template",
                    "template": self.template,
                    "context": self.context,
                }
            )
        await super().__call__(scope, receive, send)



# event_box_template = _public_template.get_template("/events_box.html")


def _get_event_box_params():
    return {"events_box": _public_template.get_template("events/events_box.html"),
            "events_context": {"events": [getattr(out_pd, e.__class__.__name__).from_pony_orm(e) for e in
                                          m.Page.select(lambda i: i.page_type == "event")]}}


includes = {
    "events": _get_event_box_params
}

_developer_shell: dict[str, PdUrl] = {
    "Управление БД": PdUrl(href="/db", is_ajax=True),
    "Мой профиль": PdUrl(href="/dev/me", is_ajax=True),
    "Скачать логи": PdUrl(href="/dev/logs"),
    "Выключить сайт": PdUrl(href="/dev/stop_server", is_ajax=True),
}
_admin_shell: dict[str, PdUrl] = {
    "Мой профиль": PdUrl(href="/admin/me", is_ajax=True),
    "Добавить админа": PdUrl(href="/admin/add_admin", is_ajax=True),
    "Добавить редактора": PdUrl(href="/admin/add_smm", is_ajax=True),
    "Добавить эксперта по направлению": PdUrl(href="/admin/add_expert", is_ajax=True),
    "Добавить страницу": PdUrl(href="/admin/add_event", is_ajax=True),
    "Написать новость": PdUrl(href="/admin/add_news", is_ajax=True),
    "Вопросы участников": PdUrl(href="/admin/look_question", is_ajax=True),
}

_smm_shell: dict[str, PdUrl] = {
    "Мой профиль": PdUrl(href="/smm/me", is_ajax=True),
    "Добавить страницу": PdUrl(href="/smm/add_event", is_ajax=True),
    "Написать новость": PdUrl(href="/smm/add_news", is_ajax=True),
    "Вопросы участников": PdUrl(href="/smm/look_question", is_ajax=True),
}
_user_shell: dict[str, PdUrl] = {
    "Мой профиль": PdUrl(href="/user/me", is_ajax=True),
    "Мои работы": PdUrl(href="/user/my_works", is_ajax=True)
}
_expert_shell: dict[str, PdUrl] = {
    "Мой профиль": PdUrl(href="/direction_expert/me", is_ajax=True),
    "Работы участников": PdUrl(href='/direction_expert/user_works', is_ajax=True)
}

_all_shells: dict[str, dict[str, PdUrl]] = {
    "Developer": _developer_shell,
    "Admin": _admin_shell,
    "Smm": _smm_shell,
    "User": _user_shell,
    "DirectionExpert": _expert_shell,
}


class MyJinja2Templates:
    """
    templates = Jinja2Templates("templates")

    return templates.TemplateResponse("index.html", {"request": request})
    """

    def __init__(self, directory: str, admin_shell: dict[str, PdUrl] = dict(),
                 access: Optional[list[AccessType]] = None) -> None:
        assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
        self.env = self.get_env(directory)
        self.admin_shell = admin_shell
        self.access = access

    def get_env(self, directory: str) -> "jinja2.Environment":
        @jinja2.contextfunction
        def url_for(context: dict, name: str, **path_params: typing.Any) -> str:
            request = context["request"]
            return request.url_for(name, **path_params)

        loader = jinja2.FileSystemLoader(directory)
        env = jinja2.Environment(loader=loader, autoescape=True)
        env.globals["url_for"] = url_for
        return env

    def get_template(self, name: str) -> "jinja2.Template":
        return self.env.get_template(name)

    def get_cooked_template(self, name: str, params: dict):
        params = self._params_addition(params)
        return self.get_template(name).render(params)

    def _params_addition(self, params: dict):
        if "request" not in params:
            raise ValueError('context must include a "request" key')
        print('Есть ли человек в request-е', hasattr(params["request"], "current_human"))
        if hasattr(params["request"], "current_human"):
            human = getattr(params["request"], "current_human")
            params['access'] = params.get('access') or human.scopes or self.access or [AccessType.PUBLIC]
            params['access_mode'] = params.get('access_mode', "")
            params['admin_shell'] = params.get('admin_shell') or _all_shells.get(
                human.__class__.__name__) or self.admin_shell
        else:
            params['access'] = params.get('access') or self.access or [AccessType.PUBLIC]
            params['access_mode'] = params.get('access_mode', "")
            params['admin_shell'] = params.get('admin_shell', self.admin_shell)

            # params['access_mode'] = params.get('access_mode') or AccessMode.LOOK
        if type(params['access']) == str:
            params['access'] = [params['access']]
        # params['access'] += ['self']
        params['access'] = [str(i) for i in params['access']]
        params['access_mode'] = str(params['access_mode'])

        return params

    def TemplateResponse(
            self,
            name: str,
            local_context: dict,
            status_code: int = 200,
            headers: dict = None,
            media_type: str = None,
            background: BackgroundTask = None,
            only_part: bool = False) -> Union[_MyTemplateResponse, JSONResponse, RedirectResponseWithBody, RedirectResponse]:
        return self.TemplateRedirectResponse(None, name, local_context, status_code=status_code, headers=headers, media_type=media_type,
                                             background=background, only_part=only_part)

    def TemplateRedirectResponse(
            self,
            url: Optional[str],
            name: str,
            local_context: dict,
            status_code: int = 300,
            headers: dict = None,
            media_type: str = None,
            background: BackgroundTask = None,
            only_part: bool = False
    ) -> Union[_MyTemplateResponse, JSONResponse, RedirectResponseWithBody, RedirectResponse]:

        template_response_params = dict(
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background
        )

        local_context = self._params_addition(local_context)
        skeleton_template = _skeleton_template
        template = self.get_template(name)

        if dict(local_context['request'].headers).get("x-part") == "basic-content":

            if status_code in code_to_resp:
                basic_data = {"request": local_context['request']}

                response_data = dict(
                    basic_data=basic_data,
                    alert=_alert_template.render(basic_data | {"alert": local_context.pop('alert', None)}),
                    admin_shell=_admin_shell_template.render(basic_data | {"pages": local_context['admin_shell']}),
                    main=template.render(local_context),
                )

                response_data = {key: val for key, val in response_data.items() if val is not None and bool(val)}

                if url is not None:
                    data = code_to_resp[300](url=url, **response_data).dict()
                    return RedirectResponseWithBody(url, data, **template_response_params)
                data = code_to_resp[status_code](**response_data).dict()
                print(data)
                return JSONResponse(
                    data, **template_response_params
                )
            context = local_context | {
                "response_status_code": status_code,
            }
            skeleton_template = template

        else:
            if url is not None:
                return RedirectResponse(url)
            # print('Генерируем весь сайт с нуля', admin_shell_template, )
            admin_shell_context = {"pages": local_context['admin_shell'], "request": local_context['request']}
            admin_shell_context = {key: val for key, val in admin_shell_context.items() if
                                   val is not None and bool(val)}
            # print(admin_shell_context)
            with db_session:
                context = dict(
                    alert=_alert_template if local_context.get('alert') else None,
                    alert_context=dict(alert=local_context.pop('alert', None)),
                    current_page=template,
                    current_page_context=local_context,
                    admin_shell=_admin_shell_template,
                    admin_shell_context=admin_shell_context,
                    request=local_context['request'],
                    # header=[SitePageMenu(name=i) for i in ["Новатор_WEB", "События", "Новости", "Результы"]],
                    title=local_context.get('title', None),
                    response_status_code=status_code,
                    current_method="POST",
                    socials=[easy_ent_pd.Socials(id=key, **val) for key, val in
                             dict(m.SimpleEntity['socials'].data).items()],
                    header_pages=[i.get_header_menu_html_code() for i in m.Page.select(lambda i: i.is_header)[:]],

                )
        return _MyTemplateResponse(
            skeleton_template,
            context,
            **template_response_params,
        )

    # def SmartResponce(
    #         self,
    #         data: str,
    #         status_code: int = 300,
    #         headers: dict = None,
    #         media_type: str = None,
    #         background: BackgroundTask = None,
    # ):
    #     pass


login_templates = MyJinja2Templates(directory="content/templates/login")
error_templates = MyJinja2Templates(directory="content/templates/errors")
db_templates = MyJinja2Templates(directory="content/templates/database", admin_shell=_developer_shell, access=[AccessType.DEVELOPER])
public_templates = MyJinja2Templates(directory="content/templates/public_temp")

developer_templates = MyJinja2Templates(directory="content/templates/developers", admin_shell=_developer_shell,
                                        access=[AccessType.DEVELOPER])
admin_templates = MyJinja2Templates(directory="content/templates/admins", admin_shell=_admin_shell,
                                    access=[AccessType.ADMIN])
smm_templates = MyJinja2Templates(directory="content/templates/smm", admin_shell=_smm_shell,
                                        access=[AccessType.SMMER])
expert_templates = MyJinja2Templates(directory="content/templates/expert", admin_shell=_expert_shell,
                                        access=[AccessType.DIRECTION_EXPERT])
user_templates = MyJinja2Templates(directory="content/templates/user", admin_shell=_user_shell,
                                        access=[AccessType.USER])

#
# class BaseAnswer:
#     ajax_answer_class: Type[BaseHTMLDataResponse] = BaseHTMLDataResponse
#     check_params_model: Type[GenResp] = GenResp
#
#     def __init__(self, *args, **kwargs):
#         self.request: Request = args[1]
#         self.data, self.all_data = self.check_params_model(*args, **kwargs)
#
#     def __new__(cls, *args, **kwargs):
#         obj = super(BaseAnswer, cls).__new__(*args, **kwargs)
#         return obj.renderer()
#
#     def renderer(self) -> Response:
#         if hasattr(self.data, "url"):
#             return self.redirect_response()
#         if dict(self.request.headers).get("x-part") == "basic-content":
#             return self.ajax_response()
#         return self.render_all_page()
#
#     def redirect_response(self):
#         pass
#
#     def ajax_response(self):
#         pass
#
#     def render_all_page(self):
#         pass
#
#
# class Ans200(BaseAnswer):
#     ajax_answer_class = Ajax200Answer
#
#     def __init__(self, request: Request,
#                  filepath: str,
#                  template_class: type,
#                  params: dict[str, Any],
#                  *args, **kwargs):
#         super(Ans200, self).__init__(self.ajax_answer_class,
#                                      request, filepath,
#                                      template_class, params,
#                                      *args, **kwargs)