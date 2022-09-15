import requests
import json
from sql import mysql
import threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.82 Safari/537.36 ',
    'Referer': 'https://cjdropshipping.com/list-detail?pageNum=1&feildType=1&isAsc=0'
    }


def get_data(page):
    data = {"page":f"{page}","size":60,"sortByParam":{"feildType":"1","isAsc":"0"}}
    return data


def get_response(data):
    requests.session().keep_alive = False
    response = json.loads(requests.post('https://cjdropshipping.com/elastic-api/product/v0.2/search', headers=headers, json=data).text)
    return response


def run_stage1(db, table, start_idx, end_idx):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    for page in range(start_idx, end_idx + 1):
        data = get_data(page)
        response = get_response(data)
        items = response['data']['content'][0]['productList']
        for item in items:
            ID = item['id']
            ID1 = ID + '--1'
            ID2 = ID + '--2'
            title = item['nameEn']
            title = title.replace("\'", "")
            title = title.replace("""\"""", "")
            image = item['bigImage'] + '?x-oss-process=image/format,jpg,image/resize,m_fill,w_179,h_190'
            if item['nowPrice'] is not None:
                price = '$' + item['nowPrice']
            else:
                price = '$' + item['sellPrice']

            conn.insertData(ID, image, title, price)
            conn.insertData(ID1, image, title, price)
            conn.insertData(ID2, image, title, price)
        print('write success', page)


def main(db, table):
    num_items = 5046
    threads = []
    threadNum = 6
    start_idx = []
    end_idx = []
    increment = int(num_items / threadNum)
    for i in range(threadNum):
        start_idx.append(1 + increment*i)
        if i == threadNum - 1:
            end_idx.append(num_items)
        else:
            end_idx.append(increment*(i+1))
    print(start_idx)
    print(end_idx)
    for i in range(1, threadNum + 1):
        threads.append(threading.Thread(target=run_stage1, args=(db, table, start_idx[i - 1], end_idx[i - 1],)))
    for t in threads:
        t.start()

    for t in threads:
        t.join()