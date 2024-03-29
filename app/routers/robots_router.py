from app.utils import templates


async def robots(request):
    return templates.TemplateResponse(
        name="robots.txt",
        media_type="text/txt",
        context={
            "request": request,
        },
    )
