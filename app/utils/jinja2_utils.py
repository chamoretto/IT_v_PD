import typing

try:
    import jinja2
except ImportError:  # pragma: nocover
    jinja2 = None  # type: ignore

from starlette.background import BackgroundTask
from starlette.responses import Response
from starlette.types import Receive, Scope, Send

from app.utils.html_utils import Alert, SitePageMenu


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

    def __init__(self, directory: str) -> None:
        assert jinja2 is not None, "jinja2 must be installed to use Jinja2Templates"
        self.env = self.get_env(directory)

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
    ) -> _MyTemplateResponse:
        if "request" not in local_context:
            raise ValueError('context must include a "request" key')
        template = self.get_template(name)
        print("========HEADERS", local_context['request'], *dict(local_context['request'].headers).items(), sep="\n")
        if dict(local_context['request'].headers).get("x-part") == "basic-content":
            context = local_context
            skeleton_template = template
        else:
            # print("template")
            # print(template)
            local_env = self.get_env("content/templates/layout")
            skeleton_template = local_env.get_template("skeleton.html")
            # print(skeleton_template)
            context = dict(
                alert=local_env.get_template("alert.html") if local_context.get('alert') else None,
                alert_context=dict(alert=local_context.pop('alert', None)),
                current_page=template,
                current_page_context=local_context,
                request=local_context['request'],
                header=[SitePageMenu(name=i) for i in ["Новатор_WEB", "События", "Новости", "Результы"]],
                title=local_context.get('title', None)
            )
        return _MyTemplateResponse(
            skeleton_template,
            context,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )


login_templates = MyJinja2Templates(directory="content/templates/login")
error_templates = MyJinja2Templates(directory="content/templates/errors")
db_templates = MyJinja2Templates(directory="content/templates/database")