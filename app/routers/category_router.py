import psycopg2
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(
    directory="app/template", autoescape=False, auto_reload=True
)


async def category(request: Request, page: int = 1) -> Response:
    cat = request.path_params["category"]
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
