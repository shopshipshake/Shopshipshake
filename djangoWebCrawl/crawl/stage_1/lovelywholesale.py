import json
import requests
from sql import mysql
import threading



class lovelywholesaleinfo(object):
    def __init__(self):
        self.post_url = 'https://soso.lovelywholesale.com/search/category/products'
        self.newoffset=1
        self.hotoffset=1
        self.newpayloaddata = {
            "category_id": "0",
            "day": "2",
            "goods_new": 1,
            "is_ad": 1,
            "limit": 50,
            "offset": self.newoffset,
            "order_by": 2,
            "topCategoryId": "1"
        }
        self.hotpayloaddata={
            "category_id": "1087",
            "is_ad": 1,
            "is_virtual": 1,
            "limit": 50,
            "offset": self.hotoffset,
            "order_by": 1,
            "original_category_id": "1087",
            "sort_by_rpc_hot": 1
        }


        self.payloadHeader = {
            'Host': 'soso.lovelywholesale.com',
            'Content-Type': 'application/json',
        }

    def get_data(self,flag,offset):

        if flag=='hot':
            self.hotoffset=offset
            dumpJsonData = json.dumps(self.hotpayloaddata)
            res = requests.post(self.post_url, data=dumpJsonData, headers=self.payloadHeader, allow_redirects=True)
            content = res.content.decode('utf-8')
            data = json.loads(content)
            return data
        elif flag=='new':
            self.newoffset = offset
            dumpJsonData = json.dumps(self.newpayloaddata)
            res = requests.post(self.post_url, data=dumpJsonData, headers=self.payloadHeader, allow_redirects=True)
            content = res.content.decode('utf-8')
            data = json.loads(content)
            return data
        else:
            return None



def run_stage1(db, table,flag, start_idx, end_idx):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    li = lovelywholesaleinfo()
    # Initialize the webpage and get the attribute from the class
    for i in range(start_idx, end_idx + 1):
        print(f"开始爬取{flag}商品第{i}页数据")
        data=li.get_data(flag,i)

        goods=data['data']['search_list']
        for good in goods:
            try:
                id = good['goods_id']

            except:
                continue
            try:
                title=good['goods_name']
                title.replace("\'", "")
            except:
                title=None
            try:
                img=good['goods_thumb']
            except:
                continue
            try:
                price=good['shop_price']
            except:
                price=None

            conn.insertData(id, img, title, price)
            id=str(id)
            id1 = id + '_1'
            conn.insertData(id1, img, title, price)
            id2 = id + '_2'
            conn.insertData(id2, img, title, price)
            print("Write Success, item", id)


def main(db, table):
    li = lovelywholesaleinfo()
    flags=['hot','new']

    for flag in flags:
        data=li.get_data(flag,1)
        pagenum= data['data']['total_page']

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
                threading.Thread(target=run_stage1, args=(db, table, flag, start_idx[i - 1], end_idx[i - 1],)))
        for t in threads:
            t.start()

        for t in threads:
            t.join()
