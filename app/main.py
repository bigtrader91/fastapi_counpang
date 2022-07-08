import random
import psycopg2


from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

from app.utils import cleanText
from app.database.database import conn
from app.service.service import items
from app.exceptions.handlers import exception_handlers
from app.middlewares import middleware


templates = Jinja2Templates(
    directory="app/template", autoescape=False, auto_reload=True
)


async def item(request):
    return templates.TemplateResponse("item.html", {"request": request})


async def search(request):
    return templates.TemplateResponse("search_item.html", {"request": request})


async def category(request):
    return templates.TemplateResponse("category.html", {"request": request})


async def sitemap(request):
    conn = psycopg2.connect(
        host="localhost",
        database="coupang",
        user="postgres",
        password="postgres",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT "productId" FROM category;""")
    category = cursor.fetchall()
    cursor.execute("""SELECT DISTINCT "productId" FROM search;""")
    search = cursor.fetchall()

    return templates.TemplateResponse(
        name="sitemap.xml",
        media_type="application/xml",
        context={
            "request": request,
            "category": category,
            "search": search,
        },
    )


async def rss(request):
    conn = psycopg2.connect(
        host="localhost",
        database="coupang",
        user="postgres",
        password="postgres",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute(
        """SELECT DISTINCT "productId", "productName",\
              "productImage",  "keyword",  "tag" FROM category;"""
    )
    category = cursor.fetchall()
    cursor.execute(
        """SELECT DISTINCT  "productId", "productName",  "productImage", \
             "keyword",  "tag" FROM search;"""
    )
    search = cursor.fetchall()
    category2 = []
    for i in category:
        temp = {}

        temp["ID"] = i[0]
        temp["상품명"] = cleanText(i[1])
        temp["이미지"] = i[2]
        temp["키워드"] = i[3]
        temp["태그"] = i[4]
        category2.append(temp)

    search2 = []
    for i in search:
        temp = {}

        temp["ID"] = i[0]
        temp["상품명"] = cleanText(i[1])
        temp["이미지"] = i[2]
        temp["키워드"] = i[3]
        temp["태그"] = i[4]
        search2.append(temp)

    return templates.TemplateResponse(
        name="rss.rss",
        media_type="application/xml",
        context={
            "request": request,
            "category2": category2,
            "search2": search2,
        },
    )


async def robots(request):
    return templates.TemplateResponse(
        name="robots.txt",
        media_type="text/txt",
        context={
            "request": request,
        },
    )


async def index(request):
    best = []
    for i in items:

        conn = psycopg2.connect(
            host="localhost",
            database="coupang",
            user="postgres",
            password="postgres",
            port=5432,
        )
        cursor = conn.cursor()
        cursor.execute(
            f"""SELECT DISTINCT "categoryName", "productName", \
                "productPrice", "productImage", "productUrl"\
                     FROM category where "categoryName"='{i}' \
                        and rank <= 4 ;"""
        )

        data = cursor.fetchall()

        temp = []
        for c in range(0, 4):
            temp_dic = {}
            temp_dic["카테고리"] = data[c][0]
            temp_dic["상품명"] = data[c][1]
            temp_dic["가격"] = data[c][2]
            temp_dic["이미지"] = data[c][3]
            temp_dic["주소"] = data[c][4]
            temp.append(temp_dic)

        best.append(temp)

    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            "best": best,
        },
    )


routes = [
    Route("/", endpoint=index),
    Route("/index", endpoint=index),
    Route("/item", endpoint=item),
    Route("/search", endpoint=search),
    Route("/category", endpoint=category),
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

# favicon_path = 'static/assets/구메구메.ico'
# from starlette.responses import FileResponse
# @app.route('/favicon.ico')
# async def favicon():
#     return FileResponse(favicon_path)


@app.route("/item/{productId:int}")
async def item(request: Request) -> Response:
    productId = request.path_params["productId"]

    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT DISTINCT * FROM category \
            where "productId"='{productId}';"""
    )
    data = cursor.fetchall()
    data = data[0]
    productId = data[1]
    productName = data[2]
    productPrice = data[3]
    productImage = data[4]
    productUrl = data[5]
    categoryName = data[6]
    keyword = data[7]
    rank = data[8]
    isRocket = data[9]
    isFreeShipping = data[10]
    tag = data[11]

    if isRocket:
        isRocket = "⭕"
    else:
        isRocket = "❌"
    if isFreeShipping:
        isFreeShipping = "⭕"
    else:
        isFreeShipping = "❌"

    cursor.execute(
        f"""SELECT DISTINCT "categoryName", "productName", \
            "productPrice", "productImage", "productUrl"\
                 FROM category where "categoryName"='{categoryName}' \
                    limit 20;"""
    )
    Related_data = cursor.fetchall()
    cnts = random.sample([i for i in range(0, len(data))], 8)
    temp = []
    for c in cnts:
        temp_dic = {}
        temp_dic["카테고리"] = Related_data[c][0]
        temp_dic["상품명"] = Related_data[c][1]
        temp_dic["가격"] = Related_data[c][2]
        temp_dic["이미지"] = Related_data[c][3]
        temp_dic["주소"] = Related_data[c][4]
        temp.append(temp_dic)

    return templates.TemplateResponse(
        name="item.html",
        context={
            "request": request,
            "productName": productName,
            "productPrice": productPrice,
            "productImage": productImage,
            "productUrl": productUrl,
            "categoryName": categoryName,
            "keyword": keyword,
            "rank": rank,
            "isRocket": isRocket,
            "isFreeShipping": isFreeShipping,
            "tag": tag,
            "temp": temp,
        },
    )


@app.route("/{category:str}")
async def category(request: Request, page: int = 1) -> Response:

    # int(request.query_params['page'])

    cat = request.path_params["category"]

    print(cat)
    cat = cat.replace("_", "/")
    conn = psycopg2.connect(
        host="localhost",
        database="coupang",
        user="postgres",
        password="postgres",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT DISTINCT "categoryName", "productName",\
             "productPrice", "productImage", "productUrl" \
                FROM category where "categoryName"='{cat}' \
                    limit 28 offset 0;"""
    )
    data = cursor.fetchall()

    temp_cat = []
    for c in range(0, 28):
        try:
            temp_dic = {}
            temp_dic["카테고리"] = data[c][0]
            temp_dic["상품명"] = data[c][1]
            temp_dic["가격"] = data[c][2]
            temp_dic["이미지"] = data[c][3]
            temp_dic["주소"] = data[c][4]
            temp_cat.append(temp_dic)
        except Exception as ex:
            print(ex)

    return templates.TemplateResponse(
        name="category.html",
        context={
            "request": request,
            "temp_cat": temp_cat,
        },
    )


@app.route("/search/{productId:int}")
async def item(request: Request) -> Response:
    productId = request.path_params["productId"]

    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT DISTINCT * FROM search where \
            "productId"='{productId}';"""
    )
    data = cursor.fetchall()
    data = data[0]
    productId = data[1]
    productName = data[2]
    productPrice = data[3]
    productImage = data[4]
    productUrl = data[5]
    keyword = data[6]
    rank = data[7]
    isRocket = data[8]
    isFreeShipping = data[9]
    tag = data[10]

    if isRocket:
        isRocket = "⭕"
    else:
        isRocket = "❌"
    if isFreeShipping:
        isFreeShipping = "⭕"
    else:
        isFreeShipping = "❌"

    cursor.execute(
        f"""SELECT DISTINCT "keyword", "productName", \
            "productPrice", "productImage", "productUrl" \
                FROM search where "keyword"='{keyword}' \
                    and "productName" != '{productName}';"""
    )
    Related_data = cursor.fetchall()
    # cnts=random.sample([i for i in range(0,len(Related_data))], 4)
    temp = []
    print(len(Related_data))
    for c in range(0, len(Related_data)):
        temp_dic = {}
        temp_dic["키워드"] = Related_data[c][0]
        temp_dic["상품명"] = Related_data[c][1]
        temp_dic["가격"] = Related_data[c][2]
        temp_dic["이미지"] = Related_data[c][3]
        temp_dic["주소"] = Related_data[c][4]
        temp.append(temp_dic)

    return templates.TemplateResponse(
        name="search_item.html",
        context={
            "request": request,
            "productName": productName,
            "productPrice": productPrice,
            "productImage": productImage,
            "productUrl": productUrl,
            "keyword": keyword,
            "rank": rank,
            "isRocket": isRocket,
            "isFreeShipping": isFreeShipping,
            "tag": tag,
            "temp": temp,
        },
    )
