import requests
import json
import urllib3
from sql import mysql

product_category = {"kitchen_supply": '1277,1283,1472',
                    "men_shoe": '1352',
                    "women_bag": '1386'}


# Get the page and convert to dictionary
def get_page_dictionary(page_num, headers, type):
    url = f'https://api.kilimall.com/ke/v1/product/search?size=40&page={page_num}&gc_id={product_category[type]}&brand_id=&order=&min=&max=&free_shipping=&have_gift=&logistic_type=&search_type=filter_search'
    urllib3.disable_warnings()
    page_text = requests.get(url=url, headers=headers, verify=False).content
    page_dictionary = json.loads(page_text)
    return page_dictionary


# The product information is contained in the returned list
def get_product_list(page_num, headers, category):
    page_dic = get_page_dictionary(page_num, headers, category)
    production_list = page_dic["data"]["products"]
    return production_list


def get_max_page(headers, category):
    page_dic = get_page_dictionary(1, headers, category)
    return page_dic["meta"]["last_page"]


def main(db, table, category):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36 '
    }
    max_page = get_max_page(headers, category)

    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()

    for page in range(1, max_page + 1):
        product_list = get_product_list(page, headers, category)

        for lists in product_list:
            try:
                id = lists["goods_id"]
                id1 = str(id) + '_1'
                id2 = str(id) + '_2'
                title = lists["name"].replace("\'", "")
                title = title.replace("""\"""", "")
                try:
                    conn.insertData(id, lists["images"]["L"][:-5], title, lists["promotion_price"])
                except:
                    continue
                conn.insertData(id1, lists["images"]["L"][:-5], title, lists["promotion_price"])
                conn.insertData(id2, lists["images"]["L"][:-5], title, lists["promotion_price"])
            except Exception as e:
                print(e)
