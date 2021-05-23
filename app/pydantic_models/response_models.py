from enum import Enum
from typing import Any, Type, Optional, Union

from pydantic import validator, root_validator

from app.pydantic_models.standart_methhods_redefinition import BaseModel
from app.utils.html_utils import Alert, shell_renderer


class ResponseType(Enum):
    HTML = "html"
    JSON = "json"
    REDIRECT = "redirect"

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
    my_response_type: ResponseType = ResponseType.HTML

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


class Ajax200Answer(BaseHTMLDataResponse):
    my_response_type: Union[ResponseType, str] = str(ResponseType.HTML)


class Ajax401Answer(BaseHTMLDataResponse):
    my_response_type: Union[ResponseType, str] = str(ResponseType.HTML)


class Ajax404Answer(BaseHTMLDataResponse):
    my_response_type: Union[ResponseType, str] = str(ResponseType.HTML)


class Ajax300Answer(BaseHTMLDataResponse):
    my_response_type: Union[ResponseType, str] = str(ResponseType.REDIRECT)
    main: Optional[str] = None
    alert: Optional[str] = None
    admin_shell: Optional[str] = None  # '<aside id="admin_shell"></aside>'
    url: str
    method: str = "GET"
    send_redirect_data: dict = dict()


class TableCell(BaseModel):
    name: str


code_to_resp: dict[int, Type[BaseResponse]] = {
    200: Ajax200Answer,
    300: Ajax300Answer,
    401: Ajax401Answer,
    404: Ajax404Answer,
}
