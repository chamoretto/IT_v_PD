from typing import Union, Any

from fastapi.responses import RedirectResponse, Response, JSONResponse
from starlette.datastructures import URL
from starlette.background import BackgroundTask
from urllib.parse import quote_plus

from app.pydantic_models.response_models import Ajax300Answer


class RedirectResponseWithBody(JSONResponse):
    def __init__(
        self,
        url: Union[str, URL],
        content: Ajax300Answer = None,
        status_code: int = 300,
        media_type: str = None,
        headers: dict = None,
        background: BackgroundTask = None,
    ) -> None:
        content = content.dict(exclude_none=True)
        super().__init__(content=content, status_code=status_code, media_type=media_type, headers=headers, background=background)
        self.headers["location"] = quote_plus(str(url), safe=":/%#?&=@[]!$&'()*+,;")
