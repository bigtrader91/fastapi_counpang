import pandas as pd
import telegram
from sqlalchemy import create_engine
import urllib.request
import joblib
import datetime
from service import 연관검색어, 쿠팡검색기, insert_data

nowT = datetime.datetime.now()
path = "/home/gumeisbuy/web/app/service/키워드모음2.pkl"

telgm_token = "1108135935:AAEzD9fUZxII258ELQm3ah_gej1E3LqLlmU"
chat_id = 1069639277
bot = telegram.Bot(token=telgm_token)
if_exists = "append"

engine = create_engine("postgresql://search:1234@localhost/coupang", echo=True)
keyword_list = joblib.load(path)

key = keyword_list.pop()
search_url = f"/v2/providers/affiliate_open_api/apis/openapi/products/search?keyword=\
    {urllib.parse.quote(key)}&limit=10&subId=wordpress"
items = 쿠팡검색기(search_url, REQUEST_METHOD="GET")

df = pd.DataFrame(items["data"]["productData"])
df["productPrice"] = df["productPrice"].apply(lambda x: format(x, ",d"))
df["tag"] = df["keyword"]
df["tag"] = df["tag"].apply(lambda x: 연관검색어(x))  # 연관검색어 열 추가
insert_data("search", df, engine, if_exists=if_exists)
bot.send_message(chat_id=chat_id, text=f"시간 : {nowT}  |  키워드 : {key}")
joblib.dump(keyword_list, path)
