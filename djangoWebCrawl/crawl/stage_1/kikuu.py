import requests
from lxml import etree
import urllib3
from sql import mysql
import threading


def get_url(headers, url):
    urllib3.disable_warnings()
    requests.session().keep_alive = False
    page_text = requests.get(url, headers=headers, verify=False).content
    page_tree = etree.HTML(page_text)
    return page_tree


class get_attribute:
    def __init__(self, url):
        self.url = url

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.107 Safari/537.36 '
        }
        self.tree = get_url(self.headers, self.url)

    def get_title(self, item_idx):
        title = self.tree.xpath(f'//ul[@class="cf"]/li[{item_idx}]/a/div[2]/text()')[0].strip()
        title = title.replace("\'", "")
        title = title.replace("""\"""", "")
        return title

    def get_price(self, item_idx):
        price = self.tree.xpath(f'//ul[@class="cf"]/li[{item_idx}]/a/p/text()')[0].strip()
        return price

    def get_item_url(self, item_idx):
        href = self.tree.xpath(f'//ul[@class="cf"]/li[{item_idx}]/a/@href')[0].strip()
        id = href[6:]
        index = id.find('-')
        id = id[:index]
        item_url = 'https://www.kikuu.com' + href

        return item_url, id

    def get_image_id(self, item_idx):
        item_url, id = self.get_item_url(item_idx)
        new_url_tree = get_url(self.headers, item_url)
        img = new_url_tree.xpath('//meta/@content')[-1][:-1].strip()
        return img, id


def run_stage1(db, table, driver, start_idx, end_idx):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    # Initialize the webpage and get the attribute from the class
    for i in range(start_idx, end_idx + 1):
        img, id = driver.get_image_id(i)
        conn.insertData(id, img, driver.get_title(i), driver.get_price(i))
        id1 = id + '_1'
        conn.insertData(id1, img, driver.get_title(i), driver.get_price(i))
        id2 = id + '_2'
        conn.insertData(id2, img, driver.get_title(i), driver.get_price(i))
        print("Write Success, item", i)


def main(db,table):
    url = "http://kikuu.com/promotion/hot"
    driver = get_attribute(url)
    num_items = len(driver.tree.xpath('//ul[@class="cf"]/li'))
    threads = []
    threadNum = 4
    start_idx = []
    end_idx = []
    increment = int(num_items / threadNum)
    for i in range(threadNum):
        start_idx.append(1 + increment*i)
        if i == threadNum - 1:
            end_idx.append(num_items)
        else:
            end_idx.append(increment*(i+1))

    for i in range(1, threadNum + 1):
        threads.append(threading.Thread(target=run_stage1, args=(db, table, driver, start_idx[i - 1], end_idx[i - 1],)))
    for t in threads:
        t.start()

    for t in threads:
        t.join()




