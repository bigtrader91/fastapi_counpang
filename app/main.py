from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.routing import Mount, Route


from app.exceptions.handlers import exception_handlers
from app.middlewares import middleware
from app.routers.robots_router import robots
from app.routers.sitemap_router import sitemap
from app.routers.index_router import index
from app.routers.category_router import category
from app.routers.item_router import item
from app.routers.search_router import search
from app.routers.검색상위종목_router import 검색상위종목

from app.routers.글자수세기_router import 글자수세기
from app.routers.유사도검사_router import 유사도검사

routes = [
    Route("/", endpoint=index),
    Route("/index", endpoint=index),
    Route("/robots.txt", endpoint=robots, methods=["GET", "POST"]),
    Route("/sitemap.xml", endpoint=sitemap, methods=["GET", "POST"]),
    Route("/검색상위종목", endpoint=검색상위종목, methods=["GET", "POST"]),
    Route("/글자수세기", endpoint=글자수세기, methods=["GET", "POST"]),
    Route("/유사도검사", endpoint=유사도검사, methods=["GET", "POST"]),
    Route("/item/{productId:int}", endpoint=item),
    Route("/search/{productId:int}", endpoint=search),
    Route("/category/{category:str}", endpoint=category),
    Mount("/static", StaticFiles(directory="app/static"), name="static"),
]


app = Starlette(
    debug=False,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
)
