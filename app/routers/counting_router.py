from app.utils import templates


async def counting(request):
    return templates.TemplateResponse(
        name="counting.html",
        context={
            "request": request,
        },
    )
