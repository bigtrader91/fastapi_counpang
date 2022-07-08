from app.database.database import conn
from app.utils import templates


async def sitemap(request):

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
