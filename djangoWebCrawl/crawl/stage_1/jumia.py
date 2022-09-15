import requests
from lxml import etree
from sql import mysql
import urllib3
import threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Safari/537.36 '
}
storeList: list = ['food-cupboard-supplies', 'household-cleaning', 'beers-wine-spirits', 'womens-make-up',
                   'fragrances-allgenders', 'office-products', 'small-appliances', 'home-kitchen',
                   'womens-fashion', 'mens-fashion', 'watches-sunglasses', 'mens-sunglasses', 'womens-accessories-sunglasses',
                   'kiddies-accessories', 'baby-diapering', 'baby-toddler-toys', 'baby-bathing-skin-care', 'baby-feeding-products',
                   'baby-gear-products', 'strength-training-equipment', 'exercise-fitness-accessories', 'team-sports',
                   'sporting-goods-outdoor-adventure']

def getHtmlTree(url):
    urllib3.disable_warnings()
    requests.session().keep_alive = False
    return etree.HTML(requests.get(url, headers).content)


def runJumia(db, table, startIdx, endIdx):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    page = 1
    for idx in range(startIdx, endIdx):
        while True:
            try:
                url = f'https://www.jumia.com.ng/{storeList[idx]}/?page={page}'
                html = getHtmlTree(url)
                IdList = html.xpath('//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article/a/@data-id')
                titleList = html.xpath('//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article/a/div[2]/h3/text()')
                imgList = html.xpath('//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article/a/div[1]/img/@data-src')
                numItem = len(IdList) # 一个网页中产品的数量
                if numItem == 0:
                    raise ValueError
                # 得到list后一一读取并存入数据库

                for i in range(numItem):
                    ID = IdList[i]
                    ID1 = ID + '--1'
                    ID2 = ID + '--2'
                    title = titleList[i]
                    title = title.replace("""\"""", "")
                    price = html.xpath(f'//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article[{i+1}]/a/div[2]/div[1]/text()')[0]
                    if price[0] != '₦':
                        price = html.xpath(f'//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article[{i+1}]/a/div[2]/div[2]/text()')[0]
                    img = imgList[i]
                    conn.insertData(ID, img, title, price)
                    conn.insertData(ID1, img, title, price)
                    conn.insertData(ID2, img, title, price)
                    print("Write Success", page, i + 1)
                page += 1

            except Exception as e:
                print(e)
                print("End of the page!")
                break


def main(db, table):
    listLen = len(storeList)
    max_page = int(listLen)
    threads = []
    threadNum = 4
    start_idx = []
    end_idx = []
    increment = int(max_page / threadNum)
    for i in range(threadNum):
        start_idx.append(increment * i)
        if i == threadNum - 1:
            end_idx.append(max_page)
        else:
            end_idx.append(increment * (i + 1))
    for i in range(1, threadNum + 1):
        threads.append(threading.Thread(target=runJumia, args=(db, table, start_idx[i - 1], end_idx[i - 1],)))
    for t in threads:
        t.start()

    for t in threads:
        t.join()
