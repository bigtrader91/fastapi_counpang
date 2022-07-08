from app.utils import templates


async def blog(request):
    return templates.TemplateResponse(
        name="blog.txt",
        context={
            "request": request,
        },
    )
