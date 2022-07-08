import requests
import pandas as pd
import json
from starlette.requests import Request
from starlette.responses import Response
from datetime import datetime, timedelta
from app.utils import templates


async def topjongmok(request: Request) -> Response:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
    }
    url = "https://finance.naver.com/sise/lastsearch2.naver"
    req = requests.get(url, headers=headers)

    topsearch = pd.read_html(req.text, encoding="utf-8")[1].dropna(subset=["순위"])
    topsearch["순위"] = topsearch["순위"].apply(lambda x: int(x))
    data = topsearch[["순위", "종목명"]].iloc[0:10, :]
    data = data.rename(columns={"종목명": "네이버"})
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
        "referer": "https://finance.daum.net/domestic",
    }

    url = "https://finance.daum.net/api/search/ranks?limit=10"

    req = requests.get(url, headers=headers)

    daum = json.loads(req.text)
    data["다음"] = [i["name"] for i in daum["data"]]
    data = list(zip(data["순위"].tolist(), data["네이버"].tolist(), data["다음"].tolist()))

    now = (datetime.now() - timedelta(hours=-9)).strftime("%Y년 %m월 %d일 %H시 %M분")
    year = datetime.now().year
    return templates.TemplateResponse(
        name="topjongmok.html",
        context={"request": request, "data": data, "now": now, "year": year},
    )
