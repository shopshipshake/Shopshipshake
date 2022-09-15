# -*- coding: utf-8 -*-
import oss2
import os
import cv2

class oss(object):
    def __init__(self):
        # Endpoint以上海为例，其它Region请按实际情况填写。
        self.endpoint = 'https://oss-cn-shanghai.aliyuncs.com'
        # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录RAM控制台创建RAM账号。
        self.access_key_id = 'Your access key'
        self.access_key_secret = 'Your access key secret'
        # 目标Bucket名称。
        self.bucket_name = ''

    def get_alibaba_url(self,imgpath,imgname):
        # 目标图片名称。若图片不在Bucket根目录，需携带文件访问路径，例如example/example.jpg。
        key = imgname
        # 指定Bucket实例，所有文件相关的方法都需要通过Bucket实例来调用。
        bucket = oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret), self.endpoint, self.bucket_name)
        # 若目标图片不在指定Bucket内，需上传图片到目标Bucket。
        bucket.put_object_from_file(key, imgpath)
        # 将图片缩放为固定宽高100 px后，再旋转0°。
        #style = 'image/resize,m_fixed,w_100,h_100/rotate,0'
        # 生成带签名的URL，并指定过期时间为10分钟。过期时间单位为秒。
        try:
            #url = bucket.sign_url('GET', key, 10 * 60, params={'x-oss-process': style})
            temp_url = bucket.sign_url('GET', key, 10 * 60)
            url=temp_url.split('?')[0]

        except:
            url=''
        return url


