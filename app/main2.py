from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from app.exceptions.handlers import exception_handlers
from app.middlewares import middleware
from app.routers.robots_router_pysyntax import robots
from app.routers.sitemap_router_pysyntax import sitemap

from app.routers.검색상위종목_router import 검색상위종목
from app.routers.유사도검사_router import 유사도검사
from app.routers.글자수세기_router import 글자수세기
from app.routers.문서자동요약_router import 문서자동요약
from app.routers.키워드_router import 키워드
import time

start1 = time.time()
routes = [
    Route("/", endpoint=키워드, methods=["GET", "POST"]),
    Route("/robots.txt", endpoint=robots, methods=["GET", "POST"]),
    Route("/sitemap.xml", endpoint=sitemap, methods=["GET", "POST"]),
    Route("/검색상위종목", endpoint=검색상위종목, methods=["GET", "POST"]),
    Route("/글자수세기", endpoint=글자수세기, methods=["GET", "POST"]),
    Route("/유사도검사", endpoint=유사도검사, methods=["GET", "POST"]),
    Route("/문서자동요약", endpoint=문서자동요약, methods=["GET", "POST"]),
    Route("/황금키워드", endpoint=키워드, methods=["GET", "POST"]),
    Mount("/static", StaticFiles(directory="app/static"), name="static"),
]


app = Starlette(
    debug=False,
    routes=routes,
    middleware=middleware,
    exception_handlers=exception_handlers,
)

end = time.time() - start1
print(end, "1")
