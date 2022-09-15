import requests
import json
import time
import re
import random
from requests import utils
from sql import mysql
from alibaba import encrypt
import threading
from alibaba import getcookies
from goto import with_goto

col_list = ["saledCount", "weight", "num_comment", "rateAverageStarLevel", "good_percent", "service",
            "wwxy", "cfmj", "zrs", "deliverySpeed", "huitou"]


def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()
    else:
        return 0


def getx5(html, key):  # 1.str参数：传入滑动html页面 2.平台key值，登录就看到了

    global aa
    T = getmidstring(html, 'NCTOKENSTR": "', '"')  # 获取网页的T值
    x5data = getmidstring(html, 'SECDATA": "', '"')  # 获取X5data

    # key = ""  # 平台key值 登录就能看到 www.ben888888.com
    url2 = "http://api.ben888888.com/api/get?key=" + \
           key + "&a=X82Y&t=" + T  # 自定义T值 淘宝检测T值 所以比较得自定义T值才能过

    i = 1
    while i < 10:  # 循环10即可，平台返回数据很快
        r = requests.get(url2)
        aa = r.text
        i += 1
        print(aa)
        if aa.find('umtoken') != -1:
            break
        else:
            time.sleep(0.3)  # 小延迟一下 避免平台卡

    data = json.loads(aa)["data"]

    bcid = data["bcid"]

    # ncSessionID 随机即可
    v1 = ''.join(random.sample('abcdefghijklmnopqrstuvwxyz1234567890', 11))
    v2 = ''.join(str(random.choice(range(10))) for _ in range(14))  # v 随机即可

    url = "https://h5api.m.taobao.com/h5/mtop.taobao.shop.impression.logo.get/1.0/_____tmd_____/slide?slidedata=%7B" \
          "%22a%22%3A%22X82Y%22%2C%22t%22%3A%22" + \
          str(data["t"]) + "%22%2C%22scene%22%3A%22" + data[
              "scene"] + "%22%2C%22p%22%3A%22%7B%5C%22ncSessionID%5C%22%3A%5C%22" + v1 + "%5C%22%2C%5C%22umidToken%5C" \
                                                                                         "%22%3A%5C%22" + \
          data["umtoken"] + "%3D%5C%22%7D%22%2C%22n%22%3A%22" + data["n"] + \
          "%22%2C%22v%22%3A1040%7D&x5secdata=" + x5data + "&v=0122" + v2

    r = requests.get(url, headers={'User-Agent': data["User-Agent"]})

    aa = r.text
    # print(aa)
    if aa.find('code":0') != -1:
        x5cookie = requests.utils.dict_from_cookiejar(
            r.cookies)  # 呆着这个cookie 取提交就可以了
        print('滑动成功')
        return x5cookie
    else:  # 这里是报错代码
        url2 = "http://api.ben888888.com/api/bc?key=" + key + "&bcid=" + bcid  # 报错接口
        r = requests.get(url2)
        print('滑动失败，报错成功', r.text)
        return 0


def get_offerId(url):
    if not url:
        return
    offerID = re.findall('offer/(.*?).html', url)
    return offerID[0]


def get_commentData(offerId, sellerId, sellerLoginId):
    comment_data = '{"fcGroup":"cbu-fc","fcName":"offerdetail-comment","serviceName":"offerCommentService",' \
                   '"params":"{' \
                   f'\\"offerId\\":{offerId},\\"sellerUserId\\":{sellerId},\\"sellerLoginId\\":\\"{sellerLoginId}\\"' \
                   '}"}'
    return comment_data


def get_offerData(offerId, businessType):
    offer_data = '{"cid":"offerdetailGetShopInfo:offerdetailGetShopInfo","methodName":"execute","params":"{\\"offerId\\":' \
                 f'{offerId},\\"businessType\\":' \
                 f'\\"{businessType}\\"' \
                 '}"}'
    return offer_data


def convert_percentToFloat(str_text):
    str_text = str_text[:-1]
    convert_float = float(str_text) / 100
    return convert_float


def decodeSpecialChar(str_text):
    if str_text[-2:] == '万+':
        str_text = str_text[:-2] + '0000'
    elif str_text[-1] == '万':
        str_text = str_text[:-1] + '0000'
    elif str_text[-1] == '+':
        str_text = str_text[:-1]
    elif str_text[0] == '<':
        str_text = str_text[1:]
    elif str_text[0] == '好':
        str_text = str_text[3:]
        str_text = convert_percentToFloat(str_text)
    elif str_text[-1] == '%':
        str_text = convert_percentToFloat(str_text)
    elif str_text[-1] == 'm':
        str_text = str_text[:-1]

    str_text = float(str_text)
    return str_text


def slideVerify(cookies, html):
    print('需要过滑动')
    zt = getx5(html, 'app key') # app key from Benben Website
    if zt != 0:
        cookies.update(zt)  # 更新cookie 把x5cookie更新到cookie里面去
    else:
        print('滑动失败，重试')


def get_commentInfo(commentDic: dict, attribute: str) -> float:
    try:
        result = decodeSpecialChar(str(commentDic['data']['model'][attribute]))
    except Exception as e:
        result = 0

    return result


def get_offerInfo(offerDic: dict, attribute: str):
    try:
        result = decodeSpecialChar(offerDic['data'][attribute]['value'])
    except:
        result = 0
    return result


@with_goto
def run_stage3(cookies, db, table, ID_tuple, url_tuple, indicator_tuple1, indicator_tuple2, start_idx, end_idx):
    global col_list
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.102 Safari/537.36"}

    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    for idx in range(start_idx, end_idx):
        try:
            label.begin
            if indicator_tuple1[idx][0] is None or indicator_tuple2[idx][0] == 0:
                i = 1  # 过滑块的验证限制: 10次
                url = url_tuple[idx][0]
                if url is None:
                    continue
                m_html = None
                offerId = get_offerId(url)
                mobile_url = f"https://m.1688.com/offer/{offerId}.html"
                while i < 10:
                    r = requests.get(mobile_url, headers=headers, cookies=cookies)
                    i += 1
                    m_html = r.text
                    if m_html.find('NCTOKENSTR') != -1:  # 出现验证码
                        slideVerify(cookies, m_html)
                    else:
                        break
                # 三个加密用的参数
                sellerId = getmidstring(m_html, "sellerUserId@", '"')
                sellerLoginId = getmidstring(m_html, 'sellerLoginId":"', '"')
                businessType = getmidstring(m_html, 'businessType":"', '"')
                # 得到30天内成交数目
                saledCount = str(getmidstring(m_html, 'saledCount":"', '"'))
                saledCount = decodeSpecialChar(saledCount)
                # 得到商品重量
                weight = float(getmidstring(m_html, 'unitWeight":', ','))
                # 加密用的字典
                commentData = get_commentData(offerId, sellerId, sellerLoginId)
                offerData = get_offerData(offerId, businessType)
                # 调用加密方法获取评论数和供应商信息的字典
                encrypt_method = encrypt.encrypt(headers, cookies, commentData, offerData)
                commentDic = encrypt_method.get_commentDic()
                offerDic = encrypt_method.get_offerDic()
                flag = 0  # Check whether the cookie is valid

                while True:
                    if flag == 4:
                        print("Cookies need to be updated!")
                        new_cookies = getcookies.get_new_cookies()
                        cookies['_m_h5_tk'] = new_cookies[0]
                        cookies['_m_h5_tk_enc'] = new_cookies[1]
                        goto.begin
                    if commentDic['ret'] != ['SUCCESS::调用成功'] and offerDic['ret'] != ['SUCCESS::调用成功']:
                        commentDic = encrypt_method.get_commentDic()
                        offerDic = encrypt_method.get_offerDic()
                        flag += 1
                        continue
                    break
                # 获取评价等三个属性的信息
                num_comment = get_commentInfo(commentDic, "commentTotalNum")
                good_percent = get_commentInfo(commentDic, "goodPercent")
                rateAverageStarLevel = get_commentInfo(commentDic, "rateAverageStarLevel")
                # 获取供应商6个属性的信息
                service = get_offerInfo(offerDic, "service")
                wwxy = get_offerInfo(offerDic, "wwxy")
                cfmj = get_offerInfo(offerDic, "cfmj")
                zrs = get_offerInfo(offerDic, "zrs")
                huitou = get_offerInfo(offerDic, "repeat")
                deliverySpeed = get_offerInfo(offerDic, "deliverySpeed")
                # 包装所有获得的信息并传入数据库
                data_list = [saledCount, weight, num_comment,
                             rateAverageStarLevel, good_percent, service, wwxy, cfmj, zrs, deliverySpeed, huitou]
                conn.update_table(col_list, data_list, "id", ID_tuple[idx][0], 3)
                print("Write Success", url)

                # 休眠一下防止访问过快有冲突
                time.sleep(0.3)

        except Exception as e:
            print(e)
            time.sleep(1)

# class TaskThread(threading.Thread):
#     def __init__(self, func, args=()):
#         super(TaskThread, self).__init__()
#         self.func = func
#         self.args = args
#
#     def run(self):
#         self.result = self.func()


def get_num_rows(db, table):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    url_tuple = conn.query_data("offer_url")
    return len(url_tuple)


def main(db, table, lowBound, upperBound):
    conn = mysql.SQL(db, table)
    conn.enter_database()
    conn.enter_table()
    ID_tuple = conn.query_data('id')
    url_tuple = conn.query_data("offer_url")
    service_tuple = conn.query_data("service")
    saledcount_tuple = conn.query_data('saledCount')
    num_rows = upperBound - lowBound + 1
    threads = []
    threadNum = 6
    start_idx = []
    end_idx = []
    increment = int(num_rows / threadNum)
    cookies = {'_m_h5_tk': '',
               '_m_h5_tk_enc': ''}
    new_cookies = getcookies.get_new_cookies()
    cookies['_m_h5_tk'] = new_cookies[0]
    cookies['_m_h5_tk_enc'] = new_cookies[1]
    for i in range(threadNum):
        start_idx.append(lowBound + increment * i)
        if i == threadNum - 1:
            end_idx.append(upperBound)
        else:
            end_idx.append(lowBound + increment * (i + 1))
    for i in range(1, threadNum + 1):
        threads.append(threading.Thread(target=run_stage3, args=(
            cookies, db, table, ID_tuple, url_tuple, service_tuple, saledcount_tuple, start_idx[i - 1], end_idx[i - 1],)))
    for t in threads:
        t.start()

    for t in threads:
        t.join()
