from database.insert import 쿠팡검색기
from database.database import insert_data
import time
import pandas as pd
items={
    '여성패션':1001,
    '남성패션':1002,
    '뷰티':1010,
    '출산/유아동':1011,
    '식품':1012,
    '주방용품':1013,
    '생활용품':1014,
    '홈인테리어':1015,
    '가전디지털':1016,
    '스포츠/레저':1017,
    '자동차용품':1018,
    '도서/음반/DVD':1019,
    '완구/취미':1020,
    '문구/오피스':1021,
    '헬스/건강식품':1024,
    '국내여행':1025,
    '해외여행':1026,
    '반려동물용품':1029,
    '유아동패션':1030
}

# dfs=[]
# for val in items.values():
#     best_url=f'/v2/providers/affiliate_open_api/apis/openapi/products/bestcategories/{val}?limit=100&subId=wordpress'
#     item_dict=쿠팡검색기(best_url)
#     time.sleep(5)
#     df=pd.DataFrame(item_dict['data'])
#     dfs.append(df)
#     print(val)
# print(dfs)
# bestcategory=pd.concat(dfs)
# bestcategory['productPrice']=bestcategory['productPrice'].apply(lambda x: format(x, ',d'))

# insert_data('category',bestcategory,if_exists='append')