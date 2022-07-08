from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.routing import Mount, Route


from app.exceptions.handlers import exception_handlers
from app.middlewares import middleware
from app.routers.robots_router import robots
from app.routers.sitemap_router import sitemap
from app.routers.rss_router import rss
from app.routers.index_router import index
from app.routers.category_router import category
from app.routers.item_router import item
from app.routers.search_router import search
from app.routers.topjongmok_router import topjongmok
from app.routers.blog_router import blog
from app.routers.counting_router import counting


routes = [
    Route("/", endpoint=index),
    Route("/index", endpoint=index),
    Route("/item/{productId:int}", endpoint=item),
    Route("/search/{productId:int}", endpoint=search),
    Route("/category/{category:str}", endpoint=category),
    Route("/robots.txt", endpoint=robots, methods=["GET", "POST"]),
    Route("/sitemap.xml", endpoint=sitemap, methods=["GET", "POST"]),
    Route("/rss", endpoint=rss, methods=["GET", "POST"]),
    Route("/topjongmok", endpoint=topjongmok, methods=["GET", "POST"]),
    Route("/counting", endpoint=counting, methods=["GET", "POST"]),
    Route("/blog", endpoint=blog),
    Mount("/static", StaticFiles(directory="app/static"), name="static"),
]


app = Starlette(
    debug=False,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
)
