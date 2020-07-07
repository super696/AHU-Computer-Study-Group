import scrapy
import re
from bs4 import BeautifulSoup

class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['http://quote.eastmoney.com/stock_list.html']

    def parse(self, response):
        #利用resonse对象的css方法获得包含股票代码的网址
        for href in response.css('a::attr(href)').extract():
            try:
                stock = re.findall(r"[s][hz]\d{6}",href)[0]
                stock = stock.upper()
                url = 'https://xueqiu.com/S/' + stock
                #新添加类，parse_stock用于获得股票信息,yield 很像迭代器
                yield scrapy.Request(url,callback = self.parse_stock)
            except:
                continue
    def parse_stock(self,response):
        #parse_stock用来获取股票信息，新建变量infoDict用来存储股票信息
        infoDict = {}
        if response == "":
            exit()
        try:
            #打开雪球网，找到东方财富点开后进行源代码分析，找到关键字<div class="stock-name">东方财富(SZ:300059)</div>    
            name = re.search(r'<div class="stock-name">(.*?)</div>', response.text).group(1)
            infoDict.update({'股票名称': name.__str__()})
            #使用正则表达式，来获取股票信息，group(1)表示获取tableHtml：后的内容
            tableHtml = re.search(r'"tableHtml":"(.*?)",', response.text).group(1)
            #使用BeautifulSoup库来解析HTML代码
            soup = BeautifulSoup(tableHtml, "html.parser")
            table = soup.table
            #股票信息标签格式 <td>最高：<span class=\"stock-rise\">70.00</span></td>，直接利用for循环获得标签内容，用字典格式保存起来
            for i in table.find_all("td"):
                line = i.text
                l = line.split("：")
                infoDict.update({l[0].__str__(): l[1].__str__()})
            yield infoDict
        except:
            print("error")
        
    #parse完毕后，将数据存入文件，通过ITEM PIPELINES结构将字典数据存入文件。
            

        
