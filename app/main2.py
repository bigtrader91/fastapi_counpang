import uvicorn
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
from app.routers.검색상위종목_router import 검색상위종목
from app.routers.blog_router import blog
from app.routers.글자수세기_router import 글자수세기


routes = [
    Route("/", endpoint=검색상위종목),
    Route("/index", endpoint=index),
    Route("/robots.txt", endpoint=robots, methods=["GET", "POST"]),
    Route("/sitemap.xml", endpoint=sitemap, methods=["GET", "POST"]),
    Route("/rss", endpoint=rss, methods=["GET", "POST"]),
    Route("/검색상위종목", endpoint=검색상위종목, methods=["GET", "POST"]),
    Route("/글자수세기", endpoint=글자수세기, methods=["GET", "POST"]),
    Mount("/static", StaticFiles(directory="app/static"), name="static"),
]


app = Starlette(
    debug=True,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
