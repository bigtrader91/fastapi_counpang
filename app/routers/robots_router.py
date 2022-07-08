from starlette.templating import Jinja2Templates

templates = Jinja2Templates(
    directory="app/template", autoescape=False, auto_reload=True
)


async def robots(request):
    return templates.TemplateResponse(
        name="robots.txt",
        media_type="text/txt",
        context={
            "request": request,
        },
    )
