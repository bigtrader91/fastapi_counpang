import random
import psycopg2

from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.staticfiles import StaticFiles

from database.database import conn
from service.service import items
from exceptions.handlers import exception_handlers
from middlewares import middleware



templates = Jinja2Templates(directory='template', autoescape=False, auto_reload=True)

async def item(request):
    return templates.TemplateResponse('item.html', {'request': request})

async def search(request):
    return templates.TemplateResponse('search_item.html', {'request': request})

async def category(request):
    return templates.TemplateResponse('category.html', {'request': request})

async def sitemap(request):
    conn = psycopg2.connect(host='localhost', database='coupang',user='postgres',password='postgres',port=5432)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT DISTINCT "productId" FROM category;""")
    category = cursor.fetchall() 
    cursor.execute(f"""SELECT DISTINCT "productId" FROM search;""")
    search = cursor.fetchall() 
    
    return templates.TemplateResponse(
        name="sitemap.xml",
        media_type='application/xml',
        context={
            "request": request,
            "category" : category,
            "search" : search,
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




routes = [
    Route('/', endpoint=index),
    Route('/index', endpoint=index),
    Route('/item', endpoint=item),
    Route('/search', endpoint=search),
    Route('/category', endpoint=category),
    Route('/robots.txt', endpoint=robots,methods=['GET', 'POST']),
    Route('/sitemap.xml', endpoint=sitemap,methods=['GET', 'POST']),
    Mount('/static', StaticFiles(directory='static'), name='static')
]



app = Starlette(debug=True, routes=routes, exception_handlers=exception_handlers)




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
    tag=data[11]


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
            'tag':tag,

            "temp":temp
        },
    )
######################################################################################

@app.route("/{category:str}")
async def category(request: Request ) -> Response:
    cat=request.path_params['category']
    cat=cat.replace("_","/")
    conn = psycopg2.connect(host='localhost', database='coupang',user='postgres',password='postgres',port=5432)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT DISTINCT "categoryName", "productName", "productPrice", "productImage", "productUrl" FROM category where "categoryName"='{cat}' limit 28;""")
    data = cursor.fetchall() 
    temp_cat=[]
    for c in range(0,28):
        try:
            temp_dic={}
            temp_dic['카테고리']=data[c][0]
            temp_dic['상품명']=data[c][1]
            temp_dic['가격']=data[c][2]
            temp_dic['이미지']=data[c][3]
            temp_dic['주소']=data[c][4]
            temp_cat.append(temp_dic)
        except Exception as ex:
            print(ex)
    
    return templates.TemplateResponse(
        name="category.html",
        context={
            "request": request,
            "temp_cat" : temp_cat

        },
    )



@app.route("/search/{productId:int}")
async def item(request: Request ) -> Response:
    productId=request.path_params['productId']
 
    cursor = conn.cursor()
    cursor.execute(f"""SELECT DISTINCT * FROM search where "productId"='{productId}';""")
    data = cursor.fetchall() 
    data=data[0]
    productId=data[1]
    productName=data[2]
    productPrice=data[3]
    productImage=data[4]
    productUrl=data[5]
    keyword=data[6]
    rank=data[7]
    isRocket=data[8]
    isFreeShipping=data[9]
    tag=data[10]


    if isRocket==True:
        isRocket='⭕'
    else:
        isRocket='❌'
    if isFreeShipping==True:
        isFreeShipping='⭕'
    else:
        isFreeShipping='❌'


    cursor.execute(f"""SELECT DISTINCT "keyword", "productName", "productPrice", "productImage", "productUrl" FROM search where "keyword"='{keyword}' ;""")
    Related_data = cursor.fetchall() 
    # cnts=random.sample([i for i in range(0,len(Related_data))], 4)
    temp=[]
    print(len(Related_data))
    for c in range(0,len(Related_data)):
        temp_dic={}
        temp_dic['키워드']=Related_data[c][0]
        temp_dic['상품명']=Related_data[c][1]
        temp_dic['가격']=Related_data[c][2]
        temp_dic['이미지']=Related_data[c][3]
        temp_dic['주소']=Related_data[c][4]
        temp.append(temp_dic)

    
    return templates.TemplateResponse(
        name="search_item.html",
        context={
            "request": request,
            "productName": productName,
            "productPrice": productPrice,
            "productImage":productImage,
            "productUrl":productUrl,
            "keyword":keyword,
            "rank":rank,
            "isRocket":isRocket,
            "isFreeShipping":isFreeShipping,
            'tag':tag,

            "temp":temp
        },
    )