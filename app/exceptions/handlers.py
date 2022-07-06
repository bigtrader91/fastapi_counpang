from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse

HTML_404_PAGE = ...
HTML_500_PAGE = ...


async def not_found(request: Request, exc: HTTPException):
    return HTMLResponse(content=HTML_404_PAGE, status_code=exc.status_code)

async def server_error(request: Request, exc: HTTPException):
    return HTMLResponse(content=HTML_500_PAGE, status_code=exc.status_code)


async def http_exception(request: Request, exc: HTTPException):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

async def excepion_error(request: Request, exc: Exception):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)

exception_handlers = {
    404: not_found,
    500: server_error,
    HTTPException: http_exception,
    Exception: excepion_error
}

