# 实现网络爬虫，爬取豆瓣250网站的相关信息
from bs4 import BeautifulSoup  # 进行网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定url，获取网页数据
import xlwt  # 进行execl操作


def main():
    baseurl = "https://movie.douban.com/top250?start="

    # 1.爬取网页
    datalist = getData(baseurl)

    # 3.保存数据
    savePath = "豆瓣电影Top250.xls"
    saveData(datalist, savePath)        # 将datalist中信息存入路径为savePath的表中



# 影片详情的链接
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）
# 影片图片
findImgsrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S让换行符包含在字符中
# 影片的片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 影片概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(10):  # 调用获取页面信息的函数·调用10次
        url = baseurl + str(i * 25)  # url地址拼接
        html = askURL(url)

        # 逐一解析数据（每获取一次网页就进行解析一次）
        soup = BeautifulSoup(html, "html.parser")  # 使用html解析器解析html
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表；
            # find_all按照一定的标准，把我们想要的数据一次性查找出来，形成一个列表。参数：找到属性包含class_="item"的div
            # print(item)       # 测试：查看电影item的全部信息
            data = []  # 保存一部电影的全部信息
            item = str(item)

            # 影片详情的链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            # print(link)           # 测试：查看一页所有电影的链接
            data.append(link)  # 添加链接

            imgSrc = re.findall(findImgsrc, item)[0]
            data.append(imgSrc)  # 添加图片

            titles = re.findall(findTitle, item)  # 片名可能只有一个中文名
            if len(titles) == 2:
                data.append(titles[0])  # 添加中文名
                otitle = titles[1].replace("/", "")  # 去掉无关符号
                data.append(otitle)  # 添加英文名
            else:
                data.append(titles[0])
                data.append('')

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 添加评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:  # 有可能有的电影没有概述
                data.append(inq)  # 添加概述
            else:
                data.append('')

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br/>', '', bd)  # 用空格替换bd字符串中的<br/>
            data.append(bd.strip())  # 去掉前后空格

            datalist.append(data)  # 把处理好的一部电影信息放入datalist中
        # print(datalist)
    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    # head模拟浏览器头部信息，向豆瓣服务器发送消息
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 81.0.4044.122Safari / 537.36"
    }  # 用户代理表示告诉豆瓣服务器，我们是什么类型的机器和浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件）
    request = urllib.request.Request(url, headers=head)  # 封装一个request对象
    html = ""
    try:
        response = urllib.request.urlopen(request)   # 发出一个请求，返回一个response对象，response对象中包含网页相关信息
        html = response.read().decode('utf-8')  # 读取response对象中的信息
        # print(html)
    except Exception as e:
        # if hasattr(e, "reason"):      # 该函数是返回对象e中是否含有reason属性
        #     print(e.reason)
        pass
    return html


# 保存数据
def saveData(datalist, savePath):
    book = xlwt.Workbook(encoding="utf-8")      # 创建book对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建表
    col =('电影详情链接', '图片链接', '影片中文名', '影片外国名', '评分', '评价人数', '概况', '相关信息')
    for i in range(8):
        sheet.write(0, i, col[i])    # 列名
    for j in range(250):
        print("爬取第%d条" %(j+1))
        data = datalist[j]
        for k in range(len(data)):
            sheet.write(j+1, k, data[k])
    book.save(savePath)


# 主函数，程序入口
if __name__ == '__main__':
    # askURL("https://movie.douban.com/top250?start=0")
    # getData("https://movie.douban.com/top250?start=0")
    main()
    print("爬取完毕！")

