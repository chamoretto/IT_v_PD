from typing import Any, Optional

from fastapi import HTTPException, Request


class ChildHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        request: Request,
        detail: Any = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers
        self.burning_request = request
