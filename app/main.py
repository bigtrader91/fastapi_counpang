from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette

from app.exceptions.handlers import exception_handlers
from app.middlewares import middleware

from app.routers.robots_router import robots
from app.routers.sitemap_router import sitemap
from app.routers.rss_router import rss
from app.routers.index_router import index
from app.routers.category_router import category
from app.routers.item_router import item
from app.routers.search_router import search

templates = Jinja2Templates(
    directory="app/template", autoescape=False, auto_reload=True
)

routes = [
    Route("/", endpoint=index),
    Route("/index", endpoint=index),
    Route("/item/{productId:int}", endpoint=item),
    Route("/search/{productId:int}", endpoint=search),
    Route("/{category:str}", endpoint=category),
    Route("/robots.txt", endpoint=robots, methods=["GET", "POST"]),
    Route("/sitemap.xml", endpoint=sitemap, methods=["GET", "POST"]),
    Route("/rss", endpoint=rss, methods=["GET", "POST"]),
    Mount("/static", StaticFiles(directory="app/static"), name="static"),
]


app = Starlette(
    debug=True,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
)
