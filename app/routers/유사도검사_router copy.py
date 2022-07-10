from app.utils import templates
from starlette.requests import Request
from starlette.responses import Response
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


async def 유사도검사(request: Request) -> Response:

    doc_list = [text1, text2]
    tfidf_vect = TfidfVectorizer()
    feature_vect = tfidf_vect.fit_transform(doc_list)

    print(feature_vect.shape)

    def cos_sim(v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    feature_vect_dense = feature_vect.todense()
    v1 = np.array(feature_vect_dense[0]).reshape(
        -1,
    )
    v2 = np.array(feature_vect_dense[1]).reshape(
        -1,
    )
    similarity_simple = cos_sim(v1, v2)
    result = round(similarity_simple * 100, 3)

    form = await request.form()
    text = form.get("text")
    # text=request.query_params['text']

    공백포함 = len(text)
    공백불포함 = len("".join(text.split()))
    return templates.TemplateResponse(
        name="유사도검사.html",
        # media_type='application/x-www-form-urlencoded',
        context={
            "request": request,
            "result": result,
        },
    )
