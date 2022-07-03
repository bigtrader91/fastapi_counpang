from time import gmtime, strftime
import json
import hmac
import hashlib
import requests

from database.insert import 쿠팡검색기
from database.database import insert_data


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


def 쿠팡검색기(URL,REQUEST_METHOD='GET'):
    
    def generateHmac(method, url, secretKey, accessKey):
        path, *query = url.split("?")
    #         os.environ["TZ"] = "GMT+0"
    #         datetime = time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'

        dateGMT = strftime('%y%m%d', gmtime())
        timeGMT = strftime('%H%M%S', gmtime())
        datetime = dateGMT + 'T' + timeGMT + 'Z'
        message = datetime + method + path + (query[0] if query else "")

        signature = hmac.new(bytes(secretKey, "utf-8"),
                            message.encode("utf-8"),
                            hashlib.sha256).hexdigest()
        return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetime, signature)
    
    REQUEST_METHOD = REQUEST_METHOD
    DOMAIN = "https://api-gateway.coupang.com"
    URL =URL
    # Replace with your own ACCESS_KEY and SECRET_KEY
    ACCESS_KEY = "c2d7d0f8-687a-43b6-9ebe-cc2f413c9a56"
    
    SECRET_KEY = "a98b7ae97ad5e63bbef6adb1e5667b9f779d72e9"


    REQUEST = { "coupangUrls": [
        "https://www.coupang.com/np/search?component=&q=good&channel=user", 
        "https://www.coupang.com/np/coupangglobal"
    ]}


    authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
    url = "{}{}".format(DOMAIN, URL)
    resposne = requests.request(method=REQUEST_METHOD, url=url,
                                headers={
                                    "Authorization": authorization,
                                    "Content-Type": "application/json"
                                },
                                data=json.dumps(REQUEST)
                                )
    rawdata=resposne.json()
    return rawdata


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