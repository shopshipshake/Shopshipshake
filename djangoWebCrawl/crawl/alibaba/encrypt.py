import time
import hashlib
from urllib import parse
import requests
import json
import urllib3


class encrypt:
    def __init__(self, headers, cookies, commentData, offerData):
        self.headers = headers
        self.cookies = cookies
        self.appkey = "12574478"
        self.cookies_m_h5_tk_split = self.cookies["_m_h5_tk"].split("_")[0]
        self.t_now = str(int(round(time.time() * 1000)))
        self.commentData = commentData
        self.offerData = offerData

    def get_sign_md5(self, data):
        sign_data = self.cookies_m_h5_tk_split + "&" + self.t_now + "&" + self.appkey + "&" + data
        sign_md5 = hashlib.md5(sign_data.encode(encoding='UTF-8')).hexdigest()
        return sign_md5

    def parse_data(self, data):
        parsedData = parse.quote(data)
        return parsedData

    def convertToDic(self,url):
        urllib3.disable_warnings()
        requests.session().keep_alive = False
        html = requests.get(url, headers=self.headers, cookies=self.cookies).text
        idx = html.find("(")
        html = html[idx + 1:]
        html = html[:-1]
        dic = json.loads(html)
        return dic

    def get_commentDic(self):
        url = 'https://h5api.m.1688.com/h5/mtop.mbox.fc.common.gateway/2.0/?jsv=2.4.8&appKey=' + self.appkey + \
              '&t=' + self.t_now + '&sign=' + self.get_sign_md5(self.commentData) + \
              '&api=mtop.mbox.fc.common.gateway&v=2.0&type=jsonp&isSec=0&timeout=20000&dataType=jsonp&callback' \
               '=mtopjsonp&data=' + self.parse_data(self.commentData)
        comment_dic = self.convertToDic(url)
        return comment_dic

    def get_offerDic(self):
        url = f'https://h5api.m.1688.com/h5/mtop.taobao.widgetservice.getjsoncomponent/1.0/?jsv=2.4.8&appKey={self.appkey}&t' \
            f'={self.t_now}&sign={self.get_sign_md5(self.offerData)}&api=mtop.taobao.widgetService.getJsonComponent&v=1.0' \
            '&type=jsonp&isSec=0&timeout=20000&dataType=jsonp&callback=mtopjsonp&data=' \
            f'{self.parse_data(self.offerData)}'
        offer_dic = self.convertToDic(url)
        return offer_dic


