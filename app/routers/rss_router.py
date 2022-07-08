import psycopg2
from app.utils import cleanText
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(
    directory="app/template", autoescape=False, auto_reload=True
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
