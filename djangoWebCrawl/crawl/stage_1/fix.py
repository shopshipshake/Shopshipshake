import json

import requests
from lxml import etree
import urllib3
from sql import mysql
import threading
from alibaba import stage2
import time


class fixinfo(object):
    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.107 Safari/537.36 '
        }

    def get_totalnum(self,url):
        content=requests.get(url,headers=self.headers).content.decode('utf8')
        json_data=json.loads(content)
        totalnum=json_data['data']['total']
        return totalnum

    def trans_url(self,url):
        totalnum=self.get_totalnum(url)
        new_url=url+f'&Nrpp={totalnum}'
        return new_url


    def get_jsondata(self,url):
        new_url=self.trans_url(url)
        content = requests.get(new_url, headers=self.headers).content.decode('utf8')
        json_data = json.loads(content)
        products=json_data['data']['products']
        return products

def run_stage1(db, table, jsondata, start_idx, end_idx):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    # Initialize the webpage and get the attribute from the class
    for i in range(start_idx, end_idx):
        data=jsondata[i]
        try:
            id=data['id']
            img=data['swapImage'][0]
            price=data['latestPriceRange']
            title=data['name']
            title.replace("\'","")
        except:
            continue

        conn.insertData(id, img, title, price)
        id1 = id + '_1'
        conn.insertData(id1, img, title, price)
        id2 = id + '_2'
        conn.insertData(id2, img, title, price)
        print("Write Success, item", i)


def main(db, table):
    mens_url = 'https://www.thefix.co.za/search/ajaxResultsList.jsp?N=ekvu4d&page=1&No=15&baseState=ekvu4d&cat=MENS&c=all'
    lady_url = 'https://www.thefix.co.za/search/ajaxResultsList.jsp?N=7ruskx&page=1&No=15&baseState=7ruskx&cat=LADIES&c=all'
    urls=[mens_url,lady_url]
    fi = fixinfo()
    for u in urls:
        total=fi.get_totalnum(u)
        jsondata=fi.get_jsondata(u)
        threads = []
        threadNum = 4
        start_idx = []
        end_idx = []
        increment = int(total / threadNum)
        for i in range(threadNum):
            start_idx.append(increment * i)
            if i == threadNum - 1:
                end_idx.append(total)
            else:
                end_idx.append(increment * (i + 1))

        for i in range(1, threadNum + 1):
            threads.append(
                threading.Thread(target=run_stage1, args=(db, table, jsondata, start_idx[i - 1], end_idx[i - 1],)))
        for t in threads:
            t.start()

        for t in threads:
            t.join()
