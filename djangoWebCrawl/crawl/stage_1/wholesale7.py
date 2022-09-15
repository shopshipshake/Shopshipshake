import json
import requests
from sql import mysql
import threading
from lxml import etree
import time

class wholesale7info(object):
    def __init__(self):

        curdate=time.strftime('%Y-%m-%d')
        self.hot_url = "https://www.wholesale7.net/hot-sale.html?page_size=80&sort_by=best_selling"
        self.new_url = f"https://www.wholesale7.net/new-products/{curdate}?sort_by=best_selling&page_size=60"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    def get_data(self, url):
        response = requests.get(url, headers=self.headers,timeout=7)
        return response.content

    def get_max_pagenum(self,url):
        pagedata = self.get_data(url)
        pagehtml = etree.HTML(pagedata)
        max_page_num = int(pagehtml.xpath('//div[@class="pages"]/a[last()-1]/text()')[0])
        return max_page_num


def run_stage1(db, table,url, start_idx, end_idx):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    wi=wholesale7info()
    # Initialize the webpage and get the attribute from the class
    for i in range(start_idx, end_idx + 1):
        print(f'正在写入第{i}页')
        pageurl=url+f'&page={i}'
        print(pageurl)
        data=wi.get_data(pageurl)
        html=etree.HTML(data)

        good_lists=html.xpath('//div[@class="classify_goods_list"]/div')

        for good in good_lists:

            try:
                id = good.xpath('./a/@data-goodsid')[0]
            except:

                id=None

            try:
                title=good.xpath('./a/img/@title')[0]
                title.replace("\'", ",")

            except:

                title=None

            try:
                price=good.xpath('./div/b/span[@class="price"]/text()')[0]

            except:
                price=None
            try:
                img=good.xpath('./a/img/@data-original')[0]
            except:

                continue

            conn.insertData(id, img, title, price)
            id=str(id)
            id1 = id + '_1'
            conn.insertData(id1, img, title, price)
            id2 = id + '_2'
            conn.insertData(id2, img, title, price)

            print("Write Success, item", id)


def main(db, table):
    wi = wholesale7info()
    urls=[wi.hot_url,wi.new_url]


    for url in urls:
        try:
            pagenum= wi.get_max_pagenum(url)
        except:
            pagenum=1


        threads = []
        threadNum = 4
        start_idx = []
        end_idx = []
        increment = int(pagenum / threadNum)
        for i in range(threadNum):
            start_idx.append(1+increment * i)
            if i == threadNum - 1:
                end_idx.append(pagenum)
            else:
                end_idx.append(increment * (i + 1))

        for i in range(1, threadNum + 1):
            threads.append(
                threading.Thread(target=run_stage1, args=(db, table,url, start_idx[i - 1], end_idx[i - 1],)))
        for t in threads:
            t.start()

        for t in threads:
            t.join()
