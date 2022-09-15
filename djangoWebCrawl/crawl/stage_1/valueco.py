import requests
from sql import mysql
from lxml import etree
import urllib3


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.159 Safari/537.36 '
}


def getmidstring(search_str, start_str, end) -> str:
    start = search_str.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = search_str.find(end, start)
        if end >= 0:
            return search_str[start:end].strip()
    else:
        return ''


def getHtmlTree(url):
    global headers
    urllib3.disable_warnings()
    html = requests.get(url, headers=headers, verify=False).content
    tree = etree.HTML(html)
    return tree


def main(db, table):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    for page in range(1, 100):
        try:
            url = f'https://valueco.co.za/store/page/{page}'
            htmlTree = getHtmlTree(url)
            for idx in range(1, 21):
                ID = getmidstring(htmlTree.xpath(f'//*[@id="main"]/ul/li[{idx}]/div/div/div[1]/a/@href')[0], 'product/',
                                  '/')
                try:
                    image = getmidstring(
                        htmlTree.xpath(f'//*[@id="main"]/ul/li[{idx}]/div/div/div[1]/a/div/img/@srcset')[0], ', ',
                        ' 2x')
                except:
                    print('no image exist')
                    continue
                title = htmlTree.xpath(f'//*[@id="main"]/ul/li[{idx}]/div/div/div[1]/a/h2/text()')[0]
                ID1 = ID + '--1'
                ID2 = ID + '--2'
                try:
                    price = htmlTree.xpath(f'//*[@id="main"]/ul/li[{idx}]/div/div/div[3]/div['
                                           f'1]/span/span/span/bdi/text()')[0]
                except IndexError:
                    price = None

                conn.insertData(ID, image, title, price)
                conn.insertData(ID1, image, title, price)
                conn.insertData(ID2, image, title, price)
                print("page", page, "item", idx)
        except Exception as e:
            print(e)
            print('End of the page')
            break

