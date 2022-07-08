from app.utils import cleanText
from app.database.database import conn
from app.utils import templates


async def rss(request):

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
