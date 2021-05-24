from enum import Enum
from typing import Any, Type, Optional, Union

from pydantic import validator, root_validator
from fastapi.templating import Jinja2Templates as FastApiJinja2Templates
from starlette.templating import Jinja2Templates as StarletteJinja2Templates
from fastapi import Request

from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.utils.html_utils import Alert, shell_renderer
from app.pydantic_models.standart_methhods_redefinition import AccessType, AccessMode


class ResponseType(Enum):
    HTML = "html"
    JSON = "json"
    REDIRECT = "redirect"
    AUTHORIZATION_REDIRECT = "authorization_redirect"
    SAVE_FILE = "save_file"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__()


print(ResponseType.HTML, [ResponseType.HTML], type(ResponseType.HTML))


class PdUrl(BaseModel):
    href: str
    is_ajax: bool = False
    is_download: bool = False

    def __str__(self) -> str:
        return self.href

    def print_ajax_class(self) -> str:
        if self.is_ajax:
            return 'class="url_as_ajax"'
        return ""

    def download(self) -> str:
        if self.is_download:
            return " download "
        return ""

    def print_url_data(self) -> str:
        return ' '.join([self.print_ajax_class(), self.download()])


class BaseResponse(BaseModel):
    my_response_type: Union[ResponseType, str] = str(ResponseType.HTML)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.__str__()


class BaseHTMLDataResponse(BaseResponse):
    my_response_type: Union[ResponseType, str]
    main: str = ""
    alert: str = ""
    admin_shell: str = '<aside id="admin_shell"></aside>'

    @root_validator(pre=True)
    def alert_validator(cls, values):
        if type(values.get('alert')) == Alert:
            values['alert'] = values['alert'].alert_renderer(values.get('request'))
        if type(values.get('admin_shell')) == dict:
            values['admin_shell'] = shell_renderer(values['admin_shell'], values.get('request'))
        return values

    @validator('my_response_type', pre=True)
    def my_response_type_validator(cls, value):
        if type(value) == ResponseType:
            return str(value)
        return value

    @classmethod
    def args_to_kwargs(cls, filepath: str, template_class: type, params: dict[str, Any], *args) -> dict[str, Any]:
        return dict(m_filepath=filepath, m_template=template_class, m_params=params)


    @classmethod
    def create(
            cls,
            my_response_type: ResponseType = None,
            alert: str = ""
    ):
        pass


class GenResp(BaseModel):
    my_response_type: Optional[ResponseType]
    m_filepath: Optional[str]  # main_filepath
    m_template: Union[Any, None]  # шаблон для генерации главной страницы
    """FastApiJinja2Templates,
                      StarletteJinja2Templates,
                      "MyJinja2Templates","""
    m_params: Optional[dict]
    alert: Optional[Alert]
    shell: Optional[dict[str, PdUrl]]
    request: Request
    model: Type[BaseHTMLDataResponse]
    url: Optional[str]
    method: Optional[str]
    access: list[AccessType] = []
    access_mode: list[AccessMode] = []


    class Config:
        arbitrary_types_allowed = True


    def create_main(self) -> Optional[str]:
        if self.m_filepath and self.m_template and self.m_params:
            return self.m_template.get_template(self.m_filepath).render(
                {"request": self.request} | self.m_params
            )
        return None

    def create_alert(self) -> Optional[str]:
        if type(self.alert) == Alert:
            return self.alert.alert_renderer(self.request)

    def create_shell(self) -> Optional[str]:
        if type(self.shell) == dict:
            return shell_renderer(self.shell, self.request)

    def __init__(self, model: Type[BaseHTMLDataResponse],
                 request: Request,
                 *args, **kwargs):
        kwargs |= {"model": model, "request": request}
        kwargs |= model.args_to_kwargs(*args)
        super(GenResp, self).__init__(**kwargs)

    def __new__(cls, *args, **kwargs) -> BaseHTMLDataResponse:
        generate_response_obj = super(GenResp, cls).__new__(cls, *args, **kwargs)
        # return generate_response_obj
        return (generate_response_obj.model(
            main=generate_response_obj.create_main(),
            alert=generate_response_obj.create_alert(),
            admin_shell=generate_response_obj.create_shell(),
            my_response_type=generate_response_obj.my_response_type or str(generate_response_obj.my_response_type),
            url=generate_response_obj.url,
            method=generate_response_obj.method,
        ), generate_response_obj)




class Ajax200Answer(BaseHTMLDataResponse):
    my_response_type: Union[ResponseType, str] = str(ResponseType.HTML)


class Ajax401Answer(BaseHTMLDataResponse):
    my_response_type: Union[ResponseType, str] = str(ResponseType.HTML)

    # @classmethod
    # def args_to_kwargs(cls, error, *args) -> dict[str, Any]:
    #     return dict(m_filepath="401.html", m_template=template_class, m_params=dict())


class Ajax404Answer(BaseHTMLDataResponse):
    my_response_type: Union[ResponseType, str] = str(ResponseType.HTML)


class Ajax300Answer(BaseHTMLDataResponse):
    my_response_type: Union[str] = str(ResponseType.REDIRECT)
    main: Optional[str] = None
    alert: Optional[str] = None
    admin_shell: Optional[str] = None  # '<aside id="admin_shell"></aside>'
    url: str
    method: str = "GET"
    send_redirect_data: dict = dict()  # данные, которые клиент должен будет отправить на сервер по указанному редиректом адресу
    data: dict = dict()  # данные, которые сервер будет должен обработать при получении редиректа

    @classmethod
    def args_to_kwargs(cls, url: str, method: str, *args) -> dict[str, Any]:
        return dict(url=url, method=method)


class TableCell(BaseModel):
    name: str


class SaveFileResponse(BaseResponse):
    my_response_type: Union[ResponseType, str] = str(ResponseType.SAVE_FILE)
    filename: str
    success: bool = True
    file_id: str


code_to_resp: dict[int, Type[BaseResponse]] = {
    200: Ajax200Answer,
    300: Ajax300Answer,
    401: Ajax401Answer,
    404: Ajax404Answer,
}
