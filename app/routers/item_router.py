import random
from starlette.requests import Request
from starlette.responses import Response
from app.database.database import conn
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(
    directory="app/template", autoescape=False, auto_reload=True
)


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
        f"""SELECT DISTINCT "categoryName", "productName", "productPrice", \
            "productImage", "productUrl" \
                FROM category \
                where "categoryName"='{categoryName}' limit 20;"""
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
