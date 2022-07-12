from app.service.service import items
from app.database.database import conn
from app.utils import templates
from config import settings


async def index(request):
    best = []
    for i in items:

        cursor = conn.cursor()
        cursor.execute(
            f"""{settings.sql_index}'{i}' \
                          and "rank" <10 ;"""
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
