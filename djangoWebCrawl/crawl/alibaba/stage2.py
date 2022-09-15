import aop
from sql import mysql
from alibaba import download_pic
from alibaba import oss
import threading
import time


class offer:
    def __init__(self, access_token):
        aop.set_default_server('gw.open.1688.com')
        aop.set_timestamp_generator(aop.get_local_timestamp())
        self.req = aop.api.AlibabaCrossSimilarOfferSearchParam()
        self.req.set_appinfo(appkey='Your app key', secret='Your Password')
        self.req.access_token = access_token

    def get_response(self, **kwargs):
        resp = self.req.get_response(timeout=20, **kwargs)
        offers_info = resp["result"]["result"][:3]
        return offers_info

    def cut_url(self, url):
        tag = url.find('?')
        return url[:tag]

    def set_offer_url(self, offer_id):
        new_url = "https://detail.1688.com/offer/" + offer_id + ".html"
        return new_url


def read_timeout_retry(img_url, id,img_path):
    i = 0
    while i <= 3:
        try:
            status = download_pic.call_download_pic(img_path,img_url,id)
            print("Retry Successfully")
            return status
        except:
            i += 1
            print("Retry", i)

    return 1


def run_stage2(offer, db, table, url_tuple, id_tuple, img_tuple, start_idx, end_idx, img_path):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()

    for i in range(start_idx, end_idx):
        img_index = i * 3
        if url_tuple[img_index][0] is not None:
            continue
        id = id_tuple[img_index][0]
        img = img_tuple[img_index][0]
        if table == 'fix' or table == 'kilimall':
            id1 = id + '_1'
            id2 = id + '_2'
        else:
            id1 = id + '--1'
            id2 = id + '--2'
        temp_id = [id, id1, id2]

        # Download product image
        try:
            status = download_pic.call_download_pic(img, img_path, id)
        except:
            # This happens because of download timeout
            status = read_timeout_retry(img, id, img_path)

        picture_url = str(img_path)
        picture_url = picture_url[9:]
        col_name = ["picture"]
        col_data = [f'{picture_url}/{id}.jpg']
        conn.update_table(col_name, col_data, "id", id, 2)
        conn.update_table(col_name, col_data, "id", id1, 2)
        conn.update_table(col_name, col_data, "id", id2, 2)

        # If we cannot get any offer information from 1688 api, then we try to upload the image to ali cloud
        # and retrieve the ali cloud url
        try:
            offer_info = offer.get_response(picUrl=img, page=1)
        except:
            numRetry = 0
            while True:
                try:
                    # The image in already in the alibaba cloud if status is 1
                    if status == 1:
                        alibaba_url = 'https://huchen.oss-cn-shanghai.aliyuncs.com/' + id + '.jpg'
                    else:
                        alibaba_url = oss.oss().get_alibaba_url(img_path + f"/{id}.jpg", f'{id}.jpg')
                    offer_info = offer.get_response(picUrl=alibaba_url, page=1)
                    break
                except Exception as e:
                    print(e)
                    if numRetry >= 3:
                        offer_info = None
                        print("retry fails!")
                        break
                    numRetry += 1
                    time.sleep(1)

        if offer_info is None:
            continue

        for j in range(len(offer_info)):
            url_1688 = offer.set_offer_url(offer_info[j]["offerId"])

            # Insert into mysql
            col_name = ["offer_url"]
            col_data = [url_1688]
            conn.update_table(col_name, col_data, "id", temp_id[j], 2)
        time.sleep(1)


def main(offer, db, table, img_path):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    id_tuple = conn.query_data("id")
    img_tuple = conn.query_data("Image")
    url_tuple = conn.query_data("offer_url")
    num_rows = len(id_tuple)
    print(num_rows)
    lb = int(input('Enter the lower bound: '))
    ub = int(input('Enter the upper bound: '))
    num_rows = ub - lb + 1
    threads = []
    threadNum = 6
    start_idx = []
    end_idx = []
    num_items = int(num_rows / 3)
    increment = int(num_items / threadNum)
    for i in range(threadNum):
        start_idx.append(int(lb/3) + increment * i)
        if i == threadNum - 1:
            end_idx.append(int(ub/3))
        else:
            end_idx.append(int(lb/3) + increment * (i+1))
    print(start_idx)
    print(end_idx)
    for i in range(1, threadNum + 1):
        threads.append(threading.Thread(target=run_stage2, args=(offer, db, table, url_tuple, id_tuple, img_tuple, start_idx[i - 1], end_idx[i - 1], img_path, )))
    for t in threads:
        t.start()

    for t in threads:
        t.join()