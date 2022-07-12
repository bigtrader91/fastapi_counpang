import sys

sys.path.append("/home/gumeisbuy/web/")
import time
import datetime
import requests
from sqlalchemy import create_engine
import telegram
from bs4 import BeautifulSoup
import hashlib
import hmac
import base64
import pandas as pd
from config import settings


class Signature:
    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(
            bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256
        )

        hash.hexdigest()
        return base64.b64encode(hash.digest())


def 문서수구하기(키워드, 기간="1m"):
    """
    키워드랑, 기간 입력( 1d, 3d, ,1m,1y 등등)
    """

    url = f"https://s.search.naver.com/p/blog/search.naver?where=blog&api_type=1&query=&{키워드}&dup_remove=1&nso=so:r,p:{기간}&a:all&nx_search_query={키워드}"
    http = requests.get(url)
    time.sleep(0.1)
    html = BeautifulSoup(http.text, "html.parser")
    문서수 = str(html).split('"')[3]
    return 문서수


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Timestamp": timestamp,
        "X-API-KEY": API_KEY,
        "X-Customer": str(CUSTOMER_ID),
        "X-Signature": signature,
    }


def insert_data(name, df, engine, if_exists="append"):
    try:
        df.to_sql(name=name, con=engine, if_exists=if_exists)
    except Exception as ex:
        print("insert_data error :", ex)


def keyword_collect(url, page):
    단어모음 = []
    for p in range(1, page + 1):
        r = requests.get(f"{url}{p}")
        time.sleep(0.2)

        html_doc = r.text
        soup = BeautifulSoup(html_doc, "html.parser")
        news_tit = soup.findAll("strong", {"class": "title"})

        for i in range(4, len(news_tit)):
            keyword = news_tit[i].get_text().replace("\n", "").split("[")[0].strip()
            단어모음.append(keyword)

    단어모음2 = []
    for 단어 in 단어모음:
        단어모음2.append(단어.replace("새글", "").replace("담기", ""))
    return 단어모음2


start = time.time()
telgm_token = settings.telgm_token
chat_id = settings.chat_id
bot = telegram.Bot(token=telgm_token)
if_exists = "replace"
page = 10
engine = create_engine(
    settings.best_uri,
    echo=True,
)
BASE_URL = "https://api.naver.com"
API_KEY = "010000000052eda533afd359cf705d708869904f47986643f559b0ae8fbfa227512aafaa01"
SECRET_KEY = "AQAAAABS7aUzr9NZz3BdcIhpkE9HEwey5V0q3nGGKrPpBFmgKw=="
CUSTOMER_ID = 2118272
uri = "/keywordstool"
method = "GET"
url_list = [
    "https://terms.naver.com/list.naver?cid=41706&categoryId=41706&so=date.dsc&viewType=&categoryType=&page=",
    "https://terms.naver.com/list.naver?cid=41700&categoryId=41700&so=date.dsc&viewType=&categoryType=&page=",
    "https://terms.naver.com/list.naver?cid=41698&categoryId=41698&so=st1.dsc&viewType=&categoryType=&page=",
    "https://terms.naver.com/list.naver?cid=41699&categoryId=41699&so=st1.dsc&viewType=&categoryType=&page=",
    "https://terms.naver.com/list.naver?cid=41697&categoryId=41697&so=st1.dsc&viewType=&categoryType=&page=",
]


단어모음3 = []
for url in url_list:
    time.sleep(1)
    단어모음2 = keyword_collect(url, page)
    단어모음3.extend(단어모음2)


df_keyword = pd.DataFrame()
for 키워드 in 단어모음3:
    try:

        키워드 = 키워드.replace(" ", "")
        req = requests.get(
            BASE_URL + uri + f"?hintKeywords={키워드}&showDetail=1",
            headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID),
        )
        time.sleep(0.5)
        df = pd.DataFrame(req.json()["keywordList"])
        df.rename(
            {
                "compIdx": "경쟁정도",
                "monthlyAveMobileClkCnt": "월평균클릭수_모바일",
                "monthlyAveMobileCtr": "월평균클릭률_모바일",
                "monthlyAvePcClkCnt": "월평균클릭수_PC",
                "monthlyAvePcCtr": "월평균클릭률_PC",
                "monthlyMobileQcCnt": "월간검색수_모바일",
                "monthlyPcQcCnt": "월간검색수_PC",
                "plAvgDepth": "월평균노출광고수",
                "relKeyword": "연관키워드",
            },
            axis=1,
            inplace=True,
        )
        df = df[
            [
                "연관키워드",
                "월간검색수_PC",
                "월간검색수_모바일",
                "월평균클릭수_PC",
                "월평균클릭수_모바일",
                "월평균클릭률_PC",
                "월평균클릭률_모바일",
                "경쟁정도",
                "월평균노출광고수",
            ]
        ]
        df_keyword = pd.concat([df_keyword, df])
    except:
        pass

df_keyword = df_keyword.drop_duplicates()
오늘 = datetime.datetime.now().strftime("%Y%m%d")
df_keyword = df_keyword.replace("< 10", "10")
df_keyword["문서수"] = df_keyword["연관키워드"].apply(문서수구하기)
df_keyword["문서수"] = df_keyword["문서수"].astype("int64")


df_keyword["월간검색수_PC"] = df_keyword["월간검색수_PC"].astype("int64")
df_keyword["월간검색수_모바일"] = df_keyword["월간검색수_모바일"].astype("int64")
df_keyword["키워드포화도"] = (
    df_keyword["문서수"] / (df_keyword["월간검색수_PC"] + df_keyword["월간검색수_모바일"]) * 100
)
df_keyword["수집일"] = 오늘
df_keyword3 = df_keyword.set_index("수집일")


insert_data("keyword", df_keyword, engine, if_exists="if_exists")
insert_data("total_keyword", df_keyword, engine, if_exists="append")
end = (time.time() - start) / 60
bot.send_message(chat_id=chat_id, text=f"황금키워드 수집 완료~! 걸린시간:{end}분")
