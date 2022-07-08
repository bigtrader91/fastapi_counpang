import psycopg2
from starlette.templating import Jinja2Templates
from app.service.service import items

templates = Jinja2Templates(
    directory="app/template", autoescape=False, auto_reload=True
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
