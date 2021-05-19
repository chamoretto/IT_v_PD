from enum import Enum
from typing import Any

from app.pydantic_models.standart_methhods_redefinition import BaseModel


class ResponseType(Enum):
    HTML = "html"
    JSON = "json"


class Ajax200Answer(BaseModel):
    my_response_type: ResponseType = "html"
    main: str = ""
    alert: str = ""
    admin_shell: str = '<aside id="admin_shell"></aside>'


class Ajax401Answer(BaseModel):
    my_response_type: ResponseType = "html"
    admin_shell: str = '<aside id="admin_shell"></aside>'
    alert: str = ""
    main: str = ""


class Ajax404Answer(BaseModel):
    my_response_type: ResponseType = "html"
    main: str = ""


class PdUrl(BaseModel):
    href: str
    is_ajax: bool = False
    is_download: bool = False

    def __str__(self):
        return self.href

    def print_ajax_class(self) -> str:
        if self.is_ajax:
            return 'class="url_as_ajax"'
        return ""

    def download(self):
        if self.is_download:
            return " download "
        return ""

    def print_url_data(self):
        return ' '.join([self.print_ajax_class(), self.download()])


code_to_resp: dict[int, Any] = {
    200: Ajax200Answer,
    401: Ajax401Answer,
    404: Ajax200Answer,
}