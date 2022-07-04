import random
import psycopg2

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.responses import FileResponse

from database.database import conn
from service.service import items
templates = Jinja2Templates(directory='template', autoescape=False, auto_reload=True)

async def item(request):
    return templates.TemplateResponse('item.html', {'request': request})

async def sitemap(request):
    conn = psycopg2.connect(host='localhost', database='coupang',user='postgres',password='postgres',port=5432)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT DISTINCT "productId" FROM category;""")
    data1 = cursor.fetchall() 
    cursor.execute(f"""SELECT DISTINCT "productId" FROM search;""")
    data2 = cursor.fetchall() 
    data=data1+data2
    return templates.TemplateResponse(
        name="sitemap.xml",
        media_type='application/xml',
        context={
            "request": request,
            "data" : data,
        },
    )
async def robots(request):
    return templates.TemplateResponse(
        name="robots.txt",
        media_type='text/txt',
        context={
            "request": request,
           
        },
    )

async def index(request):
    best=[]
    for i in items:
    
        conn = psycopg2.connect(host='localhost', database='coupang',user='postgres',password='postgres',port=5432)
        cursor = conn.cursor()
        cursor.execute(f"""SELECT DISTINCT "categoryName", "productName", "productPrice", "productImage", "productUrl" FROM category where "categoryName"='{i}' and rank <= 8 ;""")

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

###################################
class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next
    ) -> Response:
        return await call_next(request)

async def ping(request):
    return Response("Some Text")



#################################


routes = [
    Route('/', endpoint=index),
    Route('/index', endpoint=index),
    Route('/item', endpoint=item),
    Route('/robots.txt', endpoint=robots,methods=['GET', 'POST']),
    Route('/sitemap.xml', endpoint=sitemap,methods=['GET', 'POST']),
    Route('/ping', ping, methods=['GET', 'POST']),
    Mount('/static', StaticFiles(directory='static'), name='static'),
    Mount('/template', StaticFiles(directory='template'), name='template')
]




app = Starlette(
    debug=False,
    routes=routes,
    middleware=[
        Middleware(MyMiddleware),
    ]
)



@app.route("/item/{productId:int}")
async def item(request: Request ) -> Response:
    productId=request.path_params['productId']
 
    cursor = conn.cursor()
    cursor.execute(f"""SELECT DISTINCT * FROM category where "productId"='{productId}';""")
    data = cursor.fetchall() 
    data=data[0]
    productId=data[1]
    productName=data[2]
    productPrice=data[3]
    productImage=data[4]
    productUrl=data[5]
    categoryName=data[6]
    keyword=data[7]
    rank=data[8]
    isRocket=data[9]
    isFreeShipping=data[10]


    if isRocket==True:
        isRocket='⭕'
    else:
        isRocket='❌'
    if isFreeShipping==True:
        isFreeShipping='⭕'
    else:
        isFreeShipping='❌'


    cursor.execute(f"""SELECT DISTINCT "categoryName", "productName", "productPrice", "productImage", "productUrl" FROM category where "categoryName"='{categoryName}' limit 20;""")
    Related_data = cursor.fetchall() 
    cnts=random.sample([i for i in range(0,len(data))],  8)
    temp=[]
    for c in cnts:
        temp_dic={}
        temp_dic['카테고리']=Related_data[c][0]
        temp_dic['상품명']=Related_data[c][1]
        temp_dic['가격']=Related_data[c][2]
        temp_dic['이미지']=Related_data[c][3]
        temp_dic['주소']=Related_data[c][4]
        temp.append(temp_dic)

    
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

            "temp":temp
        },
    )


@app.route("/{category:str}")
async def category(request: Request ) -> Response:
    cat=request.path_params['category']
    cat=cat.replace("_","/")
    conn = psycopg2.connect(host='localhost', database='coupang',user='postgres',password='postgres',port=5432)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT DISTINCT "categoryName", "productName", "productPrice", "productImage", "productUrl" FROM category where "categoryName"='{cat}' limit 50;""")
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
