import requests
from lxml import etree
from djangoWebCrawl.crawl.sql import mysql

category = ['category-fashion-by-jumia', 'health-beauty', 'home-office', 'health-beauty', 'baby-products',
            'sporting-goods', 'toys-games', 'pet-supplies', 'patio-lawn-garden', ]


def getHTML(url):
    html = requests.get(url).content
    html = etree.HTML(html)
    return html


def main(db, table):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    for idx in range(len(category)):
        page = 0
        print('categpry is', category[idx])
        while True:
            page += 1
            print('page', page)
            url = f'https://www.zando.co.za/{category[idx]}/?page={page}'
            HTML = getHTML(url)
            itemIdx = 1
            if not HTML.xpath(
                    f'///*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article[{itemIdx}]/a/div[2]/h3/text()'):
                break
            while True:
                try:
                    title = HTML.xpath(
                        f'///*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article[{itemIdx}]/a/div[2]/h3/text()')[0]
                    price = HTML.xpath(
                        f'//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article[{itemIdx}]/a/div[2]/div[1]/text()')[0]
                    if price == "Shipped from abroad":
                        price = HTML.xpath(
                            f'//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article[{itemIdx}]/a/div[2]/div[2]/text()')[
                            0]
                    img = HTML.xpath(
                        f'//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article[{itemIdx}]/a/div[1]/img/@data-src')[0]
                    img = str(img).replace(str(img)[-5:], '')
                    ID = HTML.xpath(f'//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article[{itemIdx}]/a/@data-id')[0]
                    ID1 = ID + '--1'
                    ID2 = ID + '--2'
                    print(img)
                    conn.insertData(ID, img, title, price)
                    conn.insertData(ID1, img, title, price)
                    conn.insertData(ID2, img, title, price)
                    itemIdx += 1
                except Exception as e:
                    print(e)
                    break