from starlette.requests import Request
from starlette.responses import Response
from app.database.database import conn
from app.utils import templates
from config import settings


async def category(request: Request, page: int = 1) -> Response:
    cat = request.path_params["category"]

    cat = cat.replace("_", "/")

    cursor = conn.cursor()
    cursor.execute(
        f"""{settings.sql_category}'{cat}' \
                    limit 28 offset 0;"""
    )
    data = cursor.fetchall()

    temp_cat = []
    for c in range(0, 28):
        temp_dic = {}
        temp_dic["카테고리"] = data[c][0]
        temp_dic["상품명"] = data[c][1]
        temp_dic["가격"] = data[c][2]
        temp_dic["이미지"] = data[c][3]
        temp_dic["주소"] = data[c][4]
        temp_cat.append(temp_dic)

    return templates.TemplateResponse(
        name="category.html",
        context={
            "request": request,
            "temp_cat": temp_cat,
        },
    )
