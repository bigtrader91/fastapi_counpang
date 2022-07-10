import sys

sys.path.append("/home/gumeisbuy/web/")
import time
import pandas as pd
from sqlalchemy import create_engine
from service import 연관검색어, 쿠팡검색기, insert_data, items
import telegram
from config import settings

telgm_token = settings.telgm_token
chat_id = settings.chat_id
bot = telegram.Bot(token=telgm_token)
if_exists = "append"

engine = create_engine(
    settings.best_uri,
    echo=True,
)


dfs = []
for val in items.values():
    best_url = f"/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/{val}?limit=100&subId=wordpress&imageSize=256x256"
    item_dict = 쿠팡검색기(best_url)
    time.sleep(7)
    df = pd.DataFrame(item_dict["data"])
    dfs.append(df)

bestcategory = pd.concat(dfs)
bestcategory["productPrice"] = bestcategory["productPrice"].apply(
    lambda x: format(x, ",d")
)  # 천단위 표시
bestcategory["tag"] = bestcategory["keyword"]
bestcategory["tag"] = bestcategory["tag"].apply(lambda x: 연관검색어(x))
insert_data("category", bestcategory, engine, if_exists=if_exists)
bot.send_message(chat_id=chat_id, text="베스트 카테고리 저장 완료~!")
