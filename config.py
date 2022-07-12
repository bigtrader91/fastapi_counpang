from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    host: str = "localhost"
    database: str = "coupang"
    id: str = "postgres"
    password: str = "postgres"
    port: int = 5432
    db_uri: str = "postgresql://postgres:postgres@localhost/coupang"
    best_uri: str = "postgresql://best:1234@localhost/coupang"
    search_uri: str = "postgresql://search:1234@localhost/coupang"
    telgm_token: str = "1108135935:AAEzD9fUZxII258ELQm3ah_gej1E3LqLlmU"
    chat_id: int = 1069639277
    ACCESS_KEY: str = "c2d7d0f8-687a-43b6-9ebe-cc2f413c9a56"
    SECRET_KEY: str = "a98b7ae97ad5e63bbef6adb1e5667b9f779d72e9"

    sql_키워드: str = """SELECT DISTINCT ON("연관키워드") "연관키워드", "월간검색수_PC",\
             "월간검색수_모바일", "경쟁정도", "문서수", "키워드포화도"  \
                FROM keyword  where "키워드포화도" <10 and "월간검색수_PC" >100 and \
                    "월간검색수_모바일">100  and "경쟁정도" ='낮음' ;"""

    sql_category: str = 'SELECT DISTINCT ON("productImage") "categoryName", "productName",\
             "productPrice", "productImage", "productUrl" \
                FROM category where "categoryName"='
    sql_index: str = 'SELECT DISTINCT ON("productImage") "categoryName", "productName", \
                "productPrice", "productImage", "productUrl"\
                     FROM category where "categoryName"='
    sql_item_main: str = 'SELECT DISTINCT ON("productImage") * FROM category \
            where "productId"='
    sql_item_sub: str = 'SELECT DISTINCT ON("productImage") "categoryName", "productName", "productPrice", \
            "productImage", "productUrl" \
                FROM category \
                where "categoryName"='

    sql_search_item_main: str = (
        'SELECT DISTINCT ON("productImage") * FROM search where "productId"='
    )
    sql_search_item_sub: str = 'SELECT DISTINCT ON("productImage") "keyword", "productName", "productPrice", \
            "productImage", "productUrl" FROM search \
                where "keyword"='
    sql_rss1: str = """SELECT DISTINCT ON("productId") "productId", "productName",\
              "productImage",  "keyword",  "tag" FROM category;"""
    sql_rss2: str = """SELECT DISTINCT ON("productId")  "productId", "productName",  "productImage", \
             "keyword",  "tag" FROM search;"""
    sql_sitemap1: str = """SELECT DISTINCT ON("productId") "productId" FROM category;"""
    sql_sitemap2: str = """SELECT DISTINCT ON("productId") "productId" FROM search;"""

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
