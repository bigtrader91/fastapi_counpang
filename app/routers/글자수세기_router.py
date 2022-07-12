from click import BaseCommand
from app.utils import templates
from starlette.requests import Request
from starlette.responses import Response


async def 글자수세기(request: Request) -> Response:
    try:

        form = await request.form()
        text = form.get("text")
        # text=request.query_params['text']

        공백포함 = len(text)
        공백불포함 = len("".join(text.split()))
        return templates.TemplateResponse(
            name="글자수세기.html",
            # media_type='application/x-www-form-urlencoded',
            context={"request": request, "공백포함": 공백포함, "공백불포함": 공백불포함, "text": text},
        )

    except Exception as ex:
        print(ex)
        return templates.TemplateResponse(
            name="글자수세기.html",
            # media_type='text/plain',
            # media_type='application/x-www-form-urlencoded',
            context={
                "request": request,
            },
        )
