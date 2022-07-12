import pandas as pd

from starlette.requests import Request
from starlette.responses import Response
from datetime import datetime, timedelta
from app.utils import templates
from app.database.database import engine
from config import settings


async def 키워드(request: Request) -> Response:

    now = datetime.now().strftime("%Y%m%d")
    df = pd.read_sql_query(settings.sql_키워드, engine)

    df["TOTAL검색수"] = df["월간검색수_PC"] + df["월간검색수_모바일"]
    df = df.sort_values("TOTAL검색수", ascending=False)
    df["키워드포화도"] = df["키워드포화도"].apply(lambda x: round(x, 3))
    df = df.rename(columns={"연관키워드": "키워드"})
    count = len(df)
    data = list(
        zip(
            df["키워드"].tolist(),
            df["월간검색수_PC"].tolist(),
            df["월간검색수_모바일"].tolist(),
            df["TOTAL검색수"].tolist(),
            df["경쟁정도"].tolist(),
            df["문서수"].tolist(),
            df["키워드포화도"].tolist(),
        )
    )

    now = (datetime.now() - timedelta(hours=-9)).strftime("%Y년 %m월 %d일")

    return templates.TemplateResponse(
        name="키워드.html",
        context={"request": request, "data": data, "now": now, "count": count},
    )
