from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware


middleware = [
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=[
            "gumegume.shop",
            "*.gumegume.shop",
            "pysyntax.com",
            "*.pysyntax.com",
        ],
    ),
    # Middleware(HTTPSRedirectMiddleware),
    Middleware(CORSMiddleware, allow_origins=["*"]),
    Middleware(GZipMiddleware, minimum_size=500),
]
