# -*- coding: utf-8 -*-
import requests
import os
import urllib3


proxies = {'http': 'http://117.91.255.174:9999'}
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.77 Safari/537.36"}


def download(picPath,src, id):
    if not os.path.isdir(picPath):
        os.mkdir(picPath)
    dir = picPath+'\\' + str(id) + '.jpg'

    try:
        urllib3.disable_warnings()
        pic = requests.get(src,headers=headers,timeout=20)
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print('Sorry,image cannot downloaded, url is error{}.'.format(src))


def call_download_pic(img_url, pic_path,id):
    if not os.path.exists(pic_path + f"\{id}.jpg"):
        download(pic_path,img_url,id)
        print(f"图片{id}下载完成")
        return -1
    else:
        print("picture is already downloaded!",id)
        return 1

