import typing
from typing import Union, Optional

try:
    import jinja2
except ImportError:  # pragma: nocover
    jinja2 = None  # type: ignore

from starlette.background import BackgroundTask
from starlette.responses import Response
from starlette.types import Receive, Scope, Send
from fastapi.responses import JSONResponse

from app.utils.html_utils import Alert, SitePageMenu
from app.pydantic_models.response_models import code_to_resp


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


class MyJinja2Templates:
    """
    templates = Jinja2Templates("templates")

    return templates.TemplateResponse("index.html", {"request": request})
    """

    def __init__(self, directory: str, admin_shell: dict[str, str] = dict(), access: Optional[list[str]] = None) -> None:
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

    def TemplateResponse(
            self,
            name: str,
            local_context: dict,
            status_code: int = 200,
            headers: dict = None,
            media_type: str = None,
            background: BackgroundTask = None,
            only_part: bool = False
    ) -> Union[_MyTemplateResponse, JSONResponse]:

        if "request" not in local_context:
            raise ValueError('context must include a "request" key')

        local_context['access'] = local_context.get('access') or self.access or ["public"]
        local_context['access_mode'] = local_context.get('access_mode') or "look"
        if type(local_context['access']) == str:
            local_context['access'] = [local_context['access']]
        local_context['access'] += ['self']

        template = self.get_template(name)
        layout_env = self.get_env("content/templates/layout")
        skeleton_template = layout_env.get_template("skeleton.html")
        alert_template = layout_env.get_template("alert.html")
        admin_shell_template = layout_env.get_template("admin_shell.html")

        if dict(local_context['request'].headers).get("x-part") == "basic-content":

            if status_code in code_to_resp:
                basic_data = {"request": local_context['request']}
                response_data = dict(
                    basic_data=basic_data,
                    alert=alert_template.render(basic_data | {"alert": local_context.pop('alert', None)}),
                    admin_shell=admin_shell_template.render(basic_data | {"pages": self.admin_shell}),
                    main=template.render(local_context),
                )
                response_data = {key: val for key, val in response_data.items() if val is not None and bool(val)}
                print(*basic_data.items(), sep='\n')
                return JSONResponse(
                    code_to_resp[status_code](**response_data).dict(),
                    status_code=status_code,
                    headers=headers,
                    media_type=media_type,
                    background=background)
            print('987654567890')
            context = local_context | {"response_status_code": status_code}
            skeleton_template = template

        else:
            print('Генерируем весь сайт с нуля', admin_shell_template, )
            admin_shell_context = {"pages": self.admin_shell, "request": local_context['request']}
            admin_shell_context = {key: val for key, val in admin_shell_context.items() if val is not None and bool(val)}
            print(admin_shell_context)
            context = dict(
                alert=alert_template if local_context.get('alert') else None,
                alert_context=dict(alert=local_context.pop('alert', None)),
                current_page=template,
                current_page_context=local_context,
                admin_shell=admin_shell_template,
                admin_shell_context=admin_shell_context,
                request=local_context['request'],
                header=[SitePageMenu(name=i) for i in ["Новатор_WEB", "События", "Новости", "Результы"]],
                title=local_context.get('title', None),
                response_status_code=status_code,
                current_method="POST"
            )
        return _MyTemplateResponse(
            skeleton_template,
            context,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )


_admin_shell = {"Управление БД": "/db", "Мой профиль": "/dev/me"}

login_templates = MyJinja2Templates(directory="content/templates/login")
error_templates = MyJinja2Templates(directory="content/templates/errors")
db_templates = MyJinja2Templates(directory="content/templates/database", admin_shell=_admin_shell, access=['dev'])
public_templates = MyJinja2Templates(directory="content/templates/public_temp")

developer_templates = MyJinja2Templates(directory="content/templates/developers", admin_shell=_admin_shell, access=['dev'])
