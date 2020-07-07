import requests

def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status();  #判断状态是不是200，引发HTTPError异常
        r.encoding = r.apparent_encoding #将编码格式设置为系统能识别的格式，通常为utf-8
        return r.text
    except:
        return "产生异常"

def main():
    url = "http://www.baidu.com"
    print(getHTMLText(url))

main()
