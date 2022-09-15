import requests
import json
from sql import mysql


category_id: list = ['282', '14', '143', '27', '303', '312', '513', '540', '538', '536', '534', '603']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/93.0.4577.82 Safari/537.36 '
    }


def get_data(idx, page):
    data = {"variables":{},"query":"{products(    filter: {category_id: {in: "
                                   f"[\"{category_id[idx]}\"]"
                                   "}}"
                                   "search: \"\""
                                   "sort: {price: ASC}\n    pageSize: 20\n    "
                                   f"currentPage: {page}) "
                                   "{items {"
                                   "__typename\n      id\n      sku\n      name\n      description {\n        html\n "
                                   "  __typename\n      }\n      product_attribute\n      product_decal\n      "
                                   "image_name\n      product_image_names\n      image_name_label\n      price_range "
                                   "{\n "
                                   "minimum_price {\n          ...AllPriceFields\n          __typename\n        }\n "
                                   "__typename\n      }\n      url_key\n      meta_title\n      meta_description\n "
                                   "... on ConfigurableProduct {\n        variants {\n          product {\n "
                                   "id\n            __typename\n          }\n          __typename\n        }\n "
                                   "__typename\n      }\n      categories {\n        id\n        __typename\n      }\n "
                                   "}\n    total_count\n    aggregations {\n      attribute_code\n      count\n      "
                                   "label\n      options {\n        count\n        label\n        value\n        "
                                   "__typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment "
                                   "AllPriceFields on ProductPrice {\n  final_price {\n    value\n    __typename\n  "
                                   "}\n "
                                   "regular_price {\n    value\n    __typename\n  }\n  __typename\n}\n"}
    return data


def get_response(data):
    response = json.loads(requests.post('https://www.ackermans.co.za/graphql', headers=headers, data=data).text)
    return response


def main(db, table):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    num_category = len(category_id)
    for idx in range(num_category):
        print(idx)
        page = 1
        while True:
            try:
                data = get_data(idx, page)
                response = get_response(data)
                items = response['data']['products']['items']
                for item in items:
                    print(item)
                    ID = item['id']
                    ID1 = str(ID) + '--1'
                    ID2 = str(ID) + '--2'
                    title = item['name']
                    price = 'R' + str(item['price_range']['minimum_price']['final_price']['value'])
                    img_phase = item['product_image_names']
                    if '|' in img_phase:
                        img_phase = img_phase.split('|')[0].replace(' ','')
                    image = 'https://www.ackermans.co.za/cdn-proxy/prod-ack-cdn/product-images/prod/260_260_' + img_phase + '.jpg'
                    conn.insertData(ID, image, title, price)
                    conn.insertData(ID1, image, title, price)
                    conn.insertData(ID2, image, title, price)

                page += 1
            except Exception as e:
                print(e)
                break
