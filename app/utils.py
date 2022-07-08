import re
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(
    directory="app/template", autoescape=False, auto_reload=True
)


def cleanText(readData):
    text = re.sub("[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`'…》]", "", readData)
    return text
