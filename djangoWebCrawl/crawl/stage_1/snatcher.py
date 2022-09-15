import requests
from sql import mysql
from lxml import etree
import urllib3
import threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Safari/537.36 '
}


def getHtmlTree(url):
    global headers
    urllib3.disable_warnings()
    html = requests.get(url, headers=headers, verify=False).content
    tree = etree.HTML(html)
    return tree


def runSnatcher(db, table, startIdx, endIdx):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    for page in range(startIdx, endIdx):
        url = f'https://snatcher.co.za/best-sellers/?sort=bestselling&page={page}'
        html = getHtmlTree(url)
        titleList = html.xpath('//*[@class="product"]/article/@data-name')
        idList = html.xpath('//*[@class="product"]/article/@data-entity-id')
        priceList = html.xpath('//*[@class="product"]/article/@data-product-price')
        imgList = html.xpath('//*[@class="card-img-container"]/img[1]/@src')
        numItems = len(titleList)
        for itemIdx in range(numItems):
            ID = idList[itemIdx]
            ID1 = ID + '--1'
            ID2 = ID + '--2'
            price = priceList[itemIdx]
            title = titleList[itemIdx]
            title = title.replace("\'", "")
            title = title.replace("""\"""", "")
            img = imgList[itemIdx][:-4]
            try:
                conn.insertData(ID, img, title, price)
            except Exception as e:
                print(e)
                continue
            conn.insertData(ID1, img, title, price)
            conn.insertData(ID2, img, title, price)
            print("Write success", page, itemIdx)


def main(db, table):
    numPage = 251
    threads = []
    threadNum = 4
    start_idx = []
    end_idx = []
    increment = int(numPage / threadNum)
    for i in range(threadNum):
        start_idx.append(1 + increment*i)
        if i == threadNum - 1:
            end_idx.append(numPage)
        else:
            end_idx.append(increment*(i+1))

    for i in range(1, threadNum + 1):
        threads.append(threading.Thread(target=runSnatcher, args=(db, table, start_idx[i - 1], end_idx[i - 1],)))
    for t in threads:
        t.start()

    for t in threads:
        t.join()