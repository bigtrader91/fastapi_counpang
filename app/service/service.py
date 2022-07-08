import requests
import json
import hmac
import hashlib
import requests
from time import gmtime, strftime
import requests
from bs4 import BeautifulSoup
from config import settings


def 쿠팡검색기(URL, REQUEST_METHOD="GET"):
    def generateHmac(method, url, secretKey, accessKey):
        path, *query = url.split("?")

        dateGMT = strftime("%y%m%d", gmtime())
        timeGMT = strftime("%H%M%S", gmtime())
        datetime = dateGMT + "T" + timeGMT + "Z"
        message = datetime + method + path + (query[0] if query else "")

        signature = hmac.new(
            bytes(secretKey, "utf-8"), message.encode("utf-8"), hashlib.sha256
        ).hexdigest()
        return "CEA algorithm=HmacSHA256, access-key={},\
             signed-date={}, signature={}".format(
            accessKey, datetime, signature
        )

    REQUEST_METHOD = REQUEST_METHOD
    DOMAIN = "https://api-gateway.coupang.com"
    URL = URL
    # Replace with your own ACCESS_KEY and SECRET_KEY
    ACCESS_KEY = settings.ACCESS_KEY

    SECRET_KEY = settings.SECRET_KEY

    REQUEST = {
        "coupangUrls": [
            "https://www.coupang.com/np/search?component\
                =&q=good&channel=user",
            "https://www.coupang.com/np/coupangglobal",
        ]
    }

    authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
    url = "{}{}".format(DOMAIN, URL)
    resposne = requests.request(
        method=REQUEST_METHOD,
        url=url,
        headers={"Authorization": authorization, "Content-Type": "application/json"},
        data=json.dumps(REQUEST),
    )
    rawdata = resposne.json()
    return rawdata


def 연관검색어(keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/103.0.0.0 Safari/537.36"
    }

    url_keyword = (
        "https://search.naver.com/search.naver?where=\
            nexearch&sm=top_hty&fbm=0&ie=utf8&query="
        + keyword
    )
    req = requests.get(url_keyword, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    try:
        result = soup.find("div", {"class": "related_srch"}).find_all(
            "li", {"class": "item"}
        )
        related_srch = [i.text.strip() for i in result]
        return ", ".join(related_srch)
    except:
        return None


def insert_data(name, df, engine, if_exists="append"):
    try:
        df.to_sql(name=name, con=engine, if_exists=if_exists)
    except Exception as ex:
        print("insert_data error :", ex)


items = {
    "여성패션": 1001,
    "남성패션": 1002,
    "뷰티": 1010,
    "출산/유아동": 1011,
    "식품": 1012,
    "주방용품": 1013,
    "생활용품": 1014,
    "홈인테리어": 1015,
    "가전디지털": 1016,
    "스포츠/레저": 1017,
    "자동차용품": 1018,
    "도서/음반/DVD": 1019,
    "완구/취미": 1020,
    "문구/오피스": 1021,
    "헬스/건강식품": 1024,
    "국내여행": 1025,
    "해외여행": 1026,
    "반려동물용품": 1029,
    "유아동패션": 1030,
}
