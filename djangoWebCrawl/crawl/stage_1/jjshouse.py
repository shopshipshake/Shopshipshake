import json
import re

import requests
from sql import mysql
import threading
from lxml import etree
import time

class jjshouseinfo(object):
    def __init__(self):

        self.url="https://www.jjshouse.com/"

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    def get_data(self, url):
        response = requests.get(url, headers=self.headers,timeout=15)
        return response.content

    def get_max_pagenum(self,url):

        pagedata = self.get_data(url)
        pagehtml = etree.HTML(pagedata)
        try:
            max_page_url = pagehtml.xpath('//div[@class="page"]/a[last()]/@href')[0]
            max_page_num=re.findall('p(=)?(\d*)?',max_page_url,re.S)[-1][-1]
            max_page_num=int(max_page_num)
        except:
            max_page_num=1
        return max_page_num

    def get_target_urls_from_home(self):
        homepagedata = self.get_data(self.url)
        homepagehtml = etree.HTML(homepagedata)
        urls= homepagehtml.xpath('//span[@class="nav-not"]/../@href')+homepagehtml.xpath('//span[@class="nav-new"]/../@href')
        target_urls=[]
        for url in urls:
            target_urls.append("https://www.jjshouse.com"+url)
        target_urls=set(target_urls)
        return target_urls



def run_stage1(db, table,url, start_idx, end_idx):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    ji=jjshouseinfo()
    # print(f'当前url为{url}')
    # Initialize the webpage and get the attribute from the class
    for i in range(start_idx, end_idx + 1):

        # print(f'正在写入第{i}页')
        pageurl=url+f'p{i}'
        # print(pageurl)
        data=ji.get_data(pageurl)
        html=etree.HTML(data)

        good_lists=html.xpath('//div[@class="catpl-prod  "]')
        for good in good_lists:

            try:
                id = good.xpath('./div/@data-gid')[0]
            except:
                id=None
            try:
                title=good.xpath('./div/div[@class="pic"]/a/img[@class="list-pic alternative"]/@alt')[0]
                title.replace("\'", ",")

            except:
                title=None
            try:
                price=good.xpath('./div/div[@class="p_price "]/a/text()')[0].strip()
            except:
                price=None
            try:
                img=good.xpath('./div/div[@class="pic"]/a/img[@class="list-pic alternative"]/@src')[0]
            except:
                continue
            conn.insertData(id, img, title, price)
            id=str(id)
            id1 = id + '_1'
            conn.insertData(id1, img, title, price)
            id2 = id + '_2'
            conn.insertData(id2, img, title, price)
            # print("Write Success, item", id)


def main(db, table):
    ji = jjshouseinfo()
    urls=ji.get_target_urls_from_home()

    for url in urls:

        pagenum= ji.get_max_pagenum(url)

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
