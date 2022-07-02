import os
import hmac
import hashlib
import binascii
import os
import time
import requests
from time import gmtime, strftime
from selenium import webdriver
import chromedriver_autoinstaller
import json
import urllib.request
from summa.summarizer import summarize
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.chrome.options import Options
# # Check if chrome driver is installed or not
# chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
# driver_path = 'chromedriver.exe'
# if os.path.exists(driver_path):
#     print(f"chrom driver is insatlled: {driver_path}")
# else:
#     print(f"install the chrome driver(ver: {chrome_ver})")
#     chromedriver_autoinstaller.install(True)
    
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


def 쿠팡검색기(URL,REQUEST_METHOD='GET'):
    

    
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
