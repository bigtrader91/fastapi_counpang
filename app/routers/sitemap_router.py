import psycopg2
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(
    directory="app/template", autoescape=False, auto_reload=True
)


async def sitemap(request):
    conn = psycopg2.connect(
        host="localhost",
        database="coupang",
        user="postgres",
        password="postgres",
        port=5432,
    )
    cursor = conn.cursor()
    cursor.execute("""SELECT DISTINCT "productId" FROM category;""")
    category = cursor.fetchall()
    cursor.execute("""SELECT DISTINCT "productId" FROM search;""")
    search = cursor.fetchall()

    return templates.TemplateResponse(
        name="sitemap.xml",
        media_type="application/xml",
        context={
            "request": request,
            "category": category,
            "search": search,
        },
    )
