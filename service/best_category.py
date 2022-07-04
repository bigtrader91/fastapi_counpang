import time
import pandas as pd
from sqlalchemy import create_engine
from service import 연관검색어, 쿠팡검색기, insert_data, items

if_exists='append'

engine = create_engine("postgresql://best:1234@localhost/coupang",echo=True)

dfs=[]
for val in items.values():
    best_url=f'/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/{val}?limit=100&subId=wordpress'
    item_dict=쿠팡검색기(best_url)
    time.sleep(7)
    df=pd.DataFrame(item_dict['data'])
    dfs.append(df)

bestcategory=pd.concat(dfs)
bestcategory['productPrice']=bestcategory['productPrice'].apply(lambda x: format(x, ',d')) #천단위 표시
bestcategory['tag']=bestcategory['keyword']
bestcategory['tag']=bestcategory['tag'].apply(lambda x: 연관검색어(x)) #연관검색어 열 추가
insert_data('category',bestcategory,engine,if_exists=if_exists)