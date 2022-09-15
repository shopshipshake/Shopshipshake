import requests
from lxml import etree
import threading
from djangoWebCrawl.crawl.sql import mysql


def getHTML(url):
    html=requests.get(url).content
    html=etree.HTML(html)
    return html


def main(db,table):
    page=0
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    while True:
        page += 1
        url=f'https://www.yellowsubtrading.co.za/collections/all?page={page}'
        HTML=getHTML(url)
        itemIdx=1
        if not HTML.xpath(f'//*[@id="shopify-section-template--14312540012623__main"]/div[1]/div[2]/ul/li[{itemIdx}]/div/div[1]/h2/a/text()'):
            break
        print('page', page)
        while True:
            try:
                title=HTML.xpath(f'//*[@id="shopify-section-template--14312540012623__main"]/div[1]/div[2]/ul/li[{itemIdx}]/div/div[1]/h2/a/text()')[0]
                try:
                    price=HTML.xpath(f'//*[@id="shopify-section-template--14312540012623__main"]/div[1]/div[2]/ul/li[{itemIdx}]/div/div[1]/div[1]/div[4]/span[2]/text()')[0]
                except:
                    price = HTML.xpath(f'//*[@id="shopify-section-template--14312540012623__main"]/div[1]/div[2]/ul/li[{itemIdx}]/div/div[1]/div[1]/div[4]/span[1]/text()')[0]
                title = title.strip()
                price = price.strip()
                img = HTML.xpath(f'//*[@class="productitem"]//img[1]/@src')[itemIdx-1]
                img ="https:"+ str(img).replace(str(img)[-13:], '')
                ID=HTML.xpath(f'//*[@id="shopify-section-template--14312540012623__main"]/div[1]/div[2]/ul/li[{itemIdx}]/div/a/@href')[0]
                ID=str(ID).replace(str(ID)[0:26],'')
                print(ID)
                ID1=ID+'--1'
                ID2=ID+'--2'
                conn.insertData(ID, img, title, price)
                conn.insertData(ID1, img, title, price)
                conn.insertData(ID2, img, title, price)
                itemIdx += 1
            except :
                break