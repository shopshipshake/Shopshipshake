import requests
import json
from sql import mysql


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36 '
    }


def get_pageItem(url) -> list:
    html = requests.get(url, headers=headers).text
    html_dic : dict = json.loads(html)
    item = html_dic['listing']['items']
    return item


def main(db, table):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    for pageNo in range(1, 76):
        url = f'https://www.bidorbuy.co.za/mobilejquery/jsp/category/CategoriesAJAXHandler.jsp?pageNo={pageNo}&category=HotSelling'
        items: list = get_pageItem(url)
        for item in items:
            name = item['name']
            if 'voucher' in name or 'Voucher' in name:
                continue
            name = name.replace('\'', '')
            name = name.replace('\"', '')
            ID = str(item['id'])
            ID1 = ID + '--1'
            ID2 = ID + '--2'
            img = item['product_image_url']
            price = 'R' + item['unit_sale_price']
            conn.insertData(ID, img, name, price)
            conn.insertData(ID1, img, name, price)
            conn.insertData(ID2, img, name, price)
            print('Write success', ID)
