from app.utils import templates
from starlette.requests import Request
from starlette.responses import Response
import time

start1 = time.time()
from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np


def cos_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


async def 유사도검사(request: Request) -> Response:
    try:
        form = await request.form()
        text1 = str(form.get("text1"))
        text2 = str(form.get("text2"))
        doc_list = [text1, text2]
        start1 = time.time()
        tfidf_vect = TfidfVectorizer()
        end = time.time() - start1
        print(end, "2")

        start1 = time.time()
        feature_vect = tfidf_vect.fit_transform(doc_list)

        feature_vect_dense = feature_vect.todense()
        v1 = np.array(feature_vect_dense[0]).reshape(
            -1,
        )
        v2 = np.array(feature_vect_dense[1]).reshape(
            -1,
        )
        similarity_simple = cos_sim(v1, v2)
        sim = round(similarity_simple * 100, 2)
        result = f"{sim}%"

    except Exception as ex:
        print(ex)
        pass

    try:
        return templates.TemplateResponse(
            name="유사도검사.html",
            context={
                "request": request,
                "result": result,
                "text1": text1,
                "text2": text2,
            },
        )
    except Exception as ex:
        print(ex)
        return templates.TemplateResponse(
            name="유사도검사.html",
            context={
                "request": request,
            },
        )


end = time.time() - start1
print(end, "1")
