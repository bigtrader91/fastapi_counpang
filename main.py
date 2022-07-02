
from pyparsing import col
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, StreamingResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd
from summa.summarizer import summarize
from database.database import conn


templates = Jinja2Templates(directory='template', autoescape=False, auto_reload=True)

async def test(request):
    productName='test'

    return templates.TemplateResponse(
        name="test.html",
        context={
            "request": request,
            "productName": productName,



        },)

routes = [
    Route('/test', endpoint=test),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

app = Starlette(debug=True, routes=routes)



