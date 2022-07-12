from starlette.requests import Request
from starlette.responses import Response
from app.database.database import conn
from app.utils import templates
from config import settings


async def search(request: Request) -> Response:
    productId = request.path_params["productId"]

    cursor = conn.cursor()
    cursor.execute(f"""{settings.sql_search_item_main}'{productId}';""")
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
        f"""{settings.sql_search_item_sub}'{keyword}' \
                    and "productName" != '{productName}';"""
    )
    Related_data = cursor.fetchall()
    # cnts=random.sample([i for i in range(0,len(Related_data))], 4)
    temp = []

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
