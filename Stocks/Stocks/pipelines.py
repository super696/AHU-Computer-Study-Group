# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class StocksPipeline(object):
    def process_item(self, item, spider):
        return item

#新建一个类，用来将获得到的股票信息存入文件中

class stockPipeline(object):
    def open_spider(self,spider):
        #当使用爬虫时，pipeline所对应的方法，同时打开文件
        self.f = open('xueqiuStock.txt','w')

        #当爬虫结束时，pipeline所对应的方法，同时关闭文件
    def close_spider(self,spider):
        self.f.close()

        #对每个item项进行处理时所对应的方法
    def process_item(self,item,spider):
        try:
            line = str(dict(item))+'\n'
            self.f.write(line)
        except:
            pass
        return item
    
    
