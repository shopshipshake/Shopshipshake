import requests
from lxml import etree
import json
import urllib3
from sql import mysql
import threading
import time


def get_url(page, headers):
    url = f'https://deal-hub.co.za/collections/all?page={page}&sort_by=best-selling'
    urllib3.disable_warnings()
    requests.session().keep_alive = False
    page_text = requests.get(url, headers=headers, verify=False).content
    page_tree = etree.HTML(page_text)
    return page_tree


def trim_href(href):
    href = href[16:]
    return href


def get_js_link(href):
    js_link = 'https://deal-hub.co.za' + href + '.js'
    js_text = requests.get(js_link).content
    js_dict = json.loads(js_text)
    return js_dict


def trim_image_url(img_url):
    index = 0
    for char in img_url:
        if char == '?':
            break
        index += 1

    img_url = img_url[:-(len(img_url)) + index]
    img_url = 'http:'+img_url
    return img_url


def runDealhub(db, table, start_idx, end_idx):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36 '
    }

    #Connect to Data Base
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()

    for page in range(start_idx, end_idx):
        try:
            page_tree = get_url(page, headers)
            for item in range(1,len(page_tree.xpath('//*[@id="col-main"]/div/div'))+1):
                href = str(page_tree.xpath(f'//*[@id="col-main"]/div/div[{item}]/div/div[1]/div/div[1]/h5/a/@href')[0])
                href = trim_href(href)
                js_dic = get_js_link(href)
                id = str(js_dic["id"])
                id1 = id + '_1'
                id2 = id + '_2'
                title = js_dic["title"].replace("\'", "")
                title = title.replace("""\"""", "")
                conn.insertData(id, trim_image_url(js_dic['images'][0]), title, float(js_dic["price"])/100)
                conn.insertData(id1, trim_image_url(js_dic['images'][0]), title, float(js_dic["price"])/100)
                conn.insertData(id2, trim_image_url(js_dic['images'][0]), title, float(js_dic["price"])/100)
                print("Page",page,"item",item,"Write Success")

        except Exception as e:
            print(e)
            time.sleep(0.5)


def main(db, table):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36 '
    }
    page_tree = get_url(1, headers)
    max_page = page_tree.xpath('//*[@id="shopify-section-collection-template"]/div[2]/div/div/div[2]/div[4]/ul/li['
                               '6]/a/text()')[0]
    max_page = int(max_page)
    threads = []
    threadNum = 8
    start_idx = []
    end_idx = []
    increment = int(max_page / threadNum)
    for i in range(threadNum):
        start_idx.append(1 + increment * i)
        if i == threadNum - 1:
            end_idx.append(max_page)
        else:
            end_idx.append(increment * (i + 1))

    for i in range(1, threadNum + 1):
        threads.append(threading.Thread(target=runDealhub, args=(db, table, start_idx[i - 1], end_idx[i - 1],)))
    for t in threads:
        t.start()

    for t in threads:
        t.join()

