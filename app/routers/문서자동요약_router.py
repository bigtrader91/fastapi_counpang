from app.utils import templates
from starlette.requests import Request
from starlette.responses import Response

import numpy as np
from summa.summarizer import summarize


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


async def 문서자동요약(request: Request) -> Response:
    try:
        form = await request.form()
        입력 = str(form.get("입력"))
        입력값 = float(form.get("입력값"))
        if 입력값 > 1:
            출력 = summarize(입력, words=입력값)
        else:
            출력 = summarize(입력, ratio=입력값)

    except Exception as ex:
        print(ex)
        pass

    try:
        return templates.TemplateResponse(
            name="문서자동요약.html",
            context={
                "request": request,
                "출력": 출력,
            },
        )
    except Exception as ex:
        print(ex)
        return templates.TemplateResponse(
            name="문서자동요약.html",
            context={
                "request": request,
            },
        )


# Summa is open source software released under the The MIT License (MIT).

# Copyright (c) 2014 – now Summa NLP.
