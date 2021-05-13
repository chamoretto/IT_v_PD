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


class Ajax404Answer(BaseModel):
    _type: ResponseType = ResponseType.HTML
    main: str = ""


code_to_resp: dict[int, Any] = {
    200: Ajax200Answer,
    404: Ajax200Answer
}