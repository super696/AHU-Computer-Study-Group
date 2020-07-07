import requests
from bs4 import BeautifulSoup
import traceback
import re

def getHTMLText(url,code='utf-8'):
    try:
        #东方财富网的列表数据可以直接获取，但是爬取雪球网需要就行浏览器的伪装
        kv={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        r=requests.get(url,headers=kv,timeout=30)
        r.raise_for_status()
        r.encoding=code
        return r.text
    except:
        return "1?"

#从东方财富网爬取股票代码，并存入到列表中
def getStockList(lst,stockURL):
    html=getHTMLText(stockURL)
    soup=BeautifulSoup(html,'html.parser')
    a=soup.findAll('a')
    for i in a:
        try:
            href=i.attrs['href']
            lst_s=re.findall(r"[s][hz]\d{6}",href)[0]
            #根据雪球网的网址，股票代码前面的字母均需要变为大写
            lst.append(lst_s.upper())
        except:
            continue
    for lists in lst:
        print(lists)

#从雪球网获取每个股票代码对应的股票信息
def getStockInfo(lst,stockURL,fpath):
    count=0
    for stock in lst:
        url=stockURL+stock
        html=getHTMLText(url)
        try:
            #如果网页为空，则跳过这一次，继续循环
            if html=="":
                continue
            infoDict={}
            soup=BeautifulSoup(html,'html.parser')

            #stock_name_Info=soup.find('div',attrs={'class':'page-row'})
            #.find如果无法查找到该属性，会返回NoneType，其值为None
            #字典的更新需要一对键值对
            name=soup.find('div',attrs={'class':'stock-name'})
            if name is None:
                infoDict.update({'股票名称':'查询不到该股票'})
                #print("查询不到该股票")
            else:
                infoDict.update({'股票名称':name.text.split()[0]})

            #stockInfo=soup.find_all('div',attrs={'class':'stock-info'})[0]
            price=soup.find('div',attrs={'class':'stock-current'})
            if price is None:
                infoDict.update({'当前价格':'查询不到当前价格'})
                #print("无当前价格")
            else:
                infoDict.update({'当前价格':price.text.split()[0]})

            flags=soup.find(attrs={'class':'stock-flag'})
            if flags is None:
                infoDict.update({'当前状态':'查询不到当前状态'})
                #print("无当前状态")
            else:
                infoDict.update({'当前状态':flags.text.split()[0]})

            times=soup.find('div',attrs={'class':'stock-time'})
            if times is None:
                infoDict.update({'交易时间':'查询不到交易时间'})
                #print("无交易时间")
            else:
                infoDict.update({'交易时间':times.span.text.split()[0]})

            #keyList=stockInfo.find_all('td')
            #valueList=stockInfo.find_all('span')

            #for i in range(len(keyList)):
                #key=keyList[i].text
                #val=valueList[i].text
                #infoDict[key]=val

            with open(fpath,'a',encoding='utf-8') as f:
                f.write(str(infoDict)+'\n')
                count=count+1
                print('\r当前速度：{:.2f}%'.format(count*100/len(lst)),end="")
                #print("文件已经保存")
        except:
            traceback.print_exc()
            count=count+1
            print('\r当前速度：{:.2f}%'.format(count*100/len(lst)),end="")
            #print("2?")
            continue

def main():
    stock_list_url='http://quote.eastmoney.com/stock_list.html'
    stock_info_url='https://xueqiu.com/S/'
    output_file='F:\TecentstockInfo.txt'
    slist=[]
    getStockList(slist,stock_list_url)
    getStockInfo(slist,stock_info_url,output_file)


if __name__ == '__main__':
    main()

