from pyparsing import col
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, StreamingResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd
from summa.summarizer import summarize
from database.database import conn


templates = Jinja2Templates(directory='template', autoescape=False, auto_reload=True)

async def homepage(request):
    return templates.TemplateResponse('item.html', {'request': request})

routes = [
    Route('/', endpoint=homepage),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

app = Starlette(debug=True, routes=routes)



@app.route("/item/{cnt:int}")
async def homepage(request: Request ) -> Response:
    cnt=request.path_params['cnt']

    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM test;""")
    data = cursor.fetchall()   
    productId=data[cnt][0]
    productName=data[cnt][1]
    productPrice=data[cnt][2]
    productImage=data[cnt][3]
    productUrl=data[cnt][4]
    categoryName=data[cnt][5]
    keyword=data[cnt][6]
    rank=data[cnt][7]
    isRocket=data[cnt][8]
    isFreeShipping=data[cnt][9]
    #review=summarize(text , words=50)
    Related_item1_productName=data[cnt+1][1]
    Related_item1_productPrice=data[cnt+1][2]
    Related_item1_productImage=data[cnt+1][3]
    Related_item1_productUrl=data[cnt+1][4]
    
    Related_item2_productName=data[cnt+2][1]
    Related_item2_productPrice=data[cnt+2][2]
    Related_item2_productImage=data[cnt+2][3]
    Related_item2_productUrl=data[cnt+2][4]
        
    Related_item3_productName=data[cnt+3][1]
    Related_item3_productPrice=data[cnt+3][2]
    Related_item3_productImage=data[cnt+3][3]
    Related_item3_productUrl=data[cnt+3][4]
        
    Related_item4_productName=data[cnt+4][1]
    Related_item4_productPrice=data[cnt+4][2]
    Related_item4_productImage=data[cnt+4][3]
    Related_item4_productUrl=data[cnt+4][4]

    if isRocket==True:
        isRocket='⭕'
    else:
        isRocket='❌'
    if isFreeShipping==True:
        isFreeShipping='⭕'
    else:
        isFreeShipping='❌'

    
    return templates.TemplateResponse(
        name="item.html",
        context={
            "request": request,
            "productName": productName,
            "productPrice": productPrice,
            "productImage":productImage,
            "productUrl":productUrl,
            "categoryName":categoryName,
            "keyword":keyword,
            "rank":rank,
            "isRocket":isRocket,
            "isFreeShipping":isFreeShipping,
            # "review":review,

            "Related_item1_productName": Related_item1_productName,
            "Related_item1_productPrice": Related_item1_productPrice,
            "Related_item1_productImage": Related_item1_productImage,
            "Related_item1_productUrl":Related_item1_productUrl,

            "Related_item2_productName": Related_item2_productName,
            "Related_item2_productPrice": Related_item2_productPrice,
            "Related_item2_productImage": Related_item2_productImage,
            "Related_item2_productUrl":Related_item2_productUrl,

            "Related_item3_productName": Related_item3_productName,
            "Related_item3_productPrice": Related_item3_productPrice,
            "Related_item3_productImage": Related_item3_productImage,
            "Related_item3_productUrl":Related_item3_productUrl,

            "Related_item4_productName": Related_item4_productName,
            "Related_item4_productPrice": Related_item4_productPrice,
            "Related_item4_productImage": Related_item4_productImage,
            "Related_item4_productUrl":Related_item4_productUrl
                       


        },
    )
