from app.database.database import conn
from app.utils import templates
from config import settings


async def sitemap(request):

    cursor = conn.cursor()
    cursor.execute(settings.sql_sitemap1)
    category = cursor.fetchall()
    cursor.execute(settings.sql_sitemap2)
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
