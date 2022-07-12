from app.utils import templates


async def sitemap(request):

    return templates.TemplateResponse(
        name="sitemap_pysyntax.xml",
        media_type="application/xml",
        context={
            "request": request,
        },
    )
