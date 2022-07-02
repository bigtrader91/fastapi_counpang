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
from service import items
import psycopg2
templates = Jinja2Templates(directory='template', autoescape=False, auto_reload=True)

async def item(request):
    return templates.TemplateResponse('item.html', {'request': request})

async def index(request):
    best=[]
    for i in items:
    
        conn = psycopg2.connect(host='localhost', database='coupang',user='postgres',password='postgres',port=5432)
        cursor = conn.cursor()
        cursor.execute(f"""SELECT "categoryName", "productName", "productPrice", "productImage", "productUrl" FROM category where "categoryName"='{i}' and rank <= 8 ;""")

        data = cursor.fetchall() 
        temp=[]
        for c in range(0,8):
            temp_dic={}
            temp_dic['카테고리']=data[c][0]
            temp_dic['상품명']=data[c][1]
            temp_dic['가격']=data[c][2]
            temp_dic['이미지']=data[c][3]
            temp_dic['주소']=data[c][4]
            temp.append(temp_dic)
        
        best.append(temp)




    
    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            "best" : best,
        },
    )

routes = [
    Route('/', endpoint=index),
    Route('/index', endpoint=index),
    Route('/item', endpoint=item),
    Mount('/static', StaticFiles(directory='static'), name='static')
]




app = Starlette(debug=True, routes=routes)




@app.route("/item/{cnt:int}")
async def item(request: Request ) -> Response:
    cnt=request.path_params['cnt']

    cursor = conn.cursor()
    cursor.execute(f"""SELECT DISTINCT * FROM category;""")
    data = cursor.fetchall()   
    productId=data[cnt][1]
    productName=data[cnt][2]
    productPrice=data[cnt][3]
    productImage=data[cnt][4]
    productUrl=data[cnt][5]
    categoryName=data[cnt][6]
    keyword=data[cnt][7]
    rank=data[cnt][8]
    isRocket=data[cnt][9]
    isFreeShipping=data[cnt][10]
    #review=summarize(text , words=50)
    Related_item1_productName=data[cnt+1][2]
    Related_item1_productPrice=data[cnt+1][3]
    Related_item1_productImage=data[cnt+1][4]
    Related_item1_productUrl=data[cnt+1][5]
    
    Related_item2_productName=data[cnt+2][2]
    Related_item2_productPrice=data[cnt+2][3]
    Related_item2_productImage=data[cnt+2][4]
    Related_item2_productUrl=data[cnt+2][5]
        
    Related_item3_productName=data[cnt+3][2]
    Related_item3_productPrice=data[cnt+3][3]
    Related_item3_productImage=data[cnt+3][4]
    Related_item3_productUrl=data[cnt+3][5]
        
    Related_item4_productName=data[cnt+4][2]
    Related_item4_productPrice=data[cnt+4][3]
    Related_item4_productImage=data[cnt+4][4]
    Related_item4_productUrl=data[cnt+4][5]

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


@app.route("/{category:str}")
async def item(request: Request ) -> Response:
    cat=request.path_params['category']
    cat=cat.replace("_","/")
    print(cat)
    conn = psycopg2.connect(host='localhost', database='coupang',user='postgres',password='postgres',port=5432)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT "categoryName", "productName", "productPrice", "productImage", "productUrl" FROM category where "categoryName"='{cat}';""")
    data = cursor.fetchall() 
    temp_cat=[]
    for c in range(0,40):
        temp_dic={}
        temp_dic['카테고리']=data[c][0]
        temp_dic['상품명']=data[c][1]
        temp_dic['가격']=data[c][2]
        temp_dic['이미지']=data[c][3]
        temp_dic['주소']=data[c][4]
        temp_cat.append(temp_dic)
    
    

    
    return templates.TemplateResponse(
        name="category.html",
        context={
            "request": request,
            "temp_cat" : temp_cat

        },
    )

