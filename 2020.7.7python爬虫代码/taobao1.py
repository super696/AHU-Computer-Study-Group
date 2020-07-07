import requests
import re
'''
目标：获取淘宝搜索页面的信息，提取其中的商品名称和价格
理解： 淘宝的搜索接口 翻页的处理
技术路线：requests‐bs4‐re
'''
# 步骤1：提交商品搜索请求，循环获取页面
def get_html_text(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Mobile Safari/537.36'}
    try:
        coo = 'miid=5229591102142969968; cna=i2FOEfP0EV4CAduLBNk+eZK7; tracknick=zy%5Cu4E39%5Cu58A8%5Cu83B2%5Cu6885%5Cu7AF9; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; enc=ZwiEUvX1GmUKvUlbl5ZCNhqx%2FGgKm4bSnUa1iWPu969nyMYNf3XcjG997FQb%2FXOJ3lyQb8yK01%2FGUIr%2F9Xa9%2Fw%3D%3D; UM_distinctid=17081ccb1f44ce-06614483c3f0c2-e353165-144000-17081ccb1f520f; cookie2=1bf5dafb1605ceef57d1066d17a08664; t=7b12e9a6069e6db476bc9010cc89231a; _tb_token_=3585f370a37ae; _samesite_flag_=true; v=0; alitrackid=blog.csdn.net; lastalitrackid=blog.csdn.net; sgcookie=EP0zpZ7y0hCzuLixG7Jj4; unb=2664848101; uc3=lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dBxGJvTQxOOL50Y1M%3D&nk2=GdHjF%2BrFz5o0E7E5&id2=UU6nRR5ujv1rHw%3D%3D; csg=d5b10f78; lgc=zy%5Cu4E39%5Cu58A8%5Cu83B2%5Cu6885%5Cu7AF9; cookie17=UU6nRR5ujv1rHw%3D%3D; dnk=zy%5Cu4E39%5Cu58A8%5Cu83B2%5Cu6885%5Cu7AF9; skt=8ca72f8beb340092; existShop=MTU5Mzc0MTg1NA%3D%3D; uc4=id4=0%40U2xqITEahvffubQCQCAjO2avq%2BsM&nk4=0%40Gxj6aK63u7fpbbzFNge32XbVLGyqSfQ%3D; _cc_=V32FPkk%2Fhw%3D%3D; _l_g_=Ug%3D%3D; sg=%E7%AB%B911; _nk_=zy%5Cu4E39%5Cu58A8%5Cu83B2%5Cu6885%5Cu7AF9; cookie1=VAcIgWryxYk1HhXWfm78yxwA8YiXR%2BrVdpFg9ks1m%2BU%3D; mt=ci=90_1; uc1=existShop=false&pas=0&cookie21=Vq8l%2BKCLjhS4UhJVbhgU&cookie14=UoTV75QyYWZAbA%3D%3D&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie15=UIHiLt3xD8xYTw%3D%3D; tfstk=cMAABPNuw0mctL_J8KHlftxYAcihZsUAjrsT6VvyQzKQWMFOiLRHTCXihNrAw4C..; JSESSIONID=84DAF378EA57988F8765BCAAE48CD4D8; l=eBNhtBAlvRme1MoSBOfCnurza779SIRYSuPzaNbMiOCPOk5p5H4FWZYUvgY9CnGVh6f2R35fHFhvBeYBqIv4n5U62j-laskmn; isg=BIuL35ZmUaybToltwgWBFsqhGi91IJ-i5SW0uf2IYkohHKt-hfNU8lC-9hzyOfea'
        cookies = {}
        for line in coo.split(';'):  # 浏览器伪装
            name, value = line.strip().split('=', 1)
            cookies[name] = value
        r = requests.get(url, cookies=cookies, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''
 
 
# 步骤2：对于每个页面，提取商品名称和价格信息
def parse_page(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)  # findall搜索全部字符串，viex_price是源代码中表价格的值，后面的字符串为数字和点组成的字符串
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)  # 找到该字符串和后面符合正则表达式的字符串
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])  # re.split() 将一个字符串按照正则表达式匹配结果进行分割，返回列表类型
            title = eval(tlt[i].split(':')[1])  # 将re获得的字符串以：为界限分为两个字符串,并取第二个字符串
            ilt.append([price, title])
    except:
        print('')
 
# 步骤3：将信息输出到屏幕上
def print_goods_list(ilt):
    tplt = "{:4}\t{:8}\t{:16}"  # 长度为多少
    print(tplt.format('序号', '价格', '名称'))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))
 
def main():
    goods = '书包'
    depth = 10  # 要爬取几页
    start_url = 'https://s.taobao.com/search?q=' + goods
    info_list = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44*i)  # 44是淘宝每个页面呈现的宝贝数量
            html = get_html_text(url)
            parse_page(info_list, html)
        except:
            continue
    print_goods_list(info_list)
 
main()

