# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class AlibabaCrossSimilarOfferSearchParam(BaseApi):
    """跨境场景根据图片搜索相似品

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.linkplus&n=alibaba.cross.similar.offer.search&v=1&cat=linkplus

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.access_token = None
        self.picUrl = None
        self.page = None
        self.priceMin = None
        self.priceMax = None
        self.sortFields = None
        self.cpsFirst = None
        self.mediaId = None
        self.mediaZoneId = None
        self.categoryID = None


    def get_api_uri(self):
        return '1/com.alibaba.linkplus/alibaba.cross.similar.offer.search'

    def get_required_params(self):
        #return ['picUrl', 'page', 'priceMin', 'priceMax', 'sortFields', 'cpsFirst', 'mediaId', 'mediaZoneId', 'categoryID']
        return ['picUrl', 'page']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return True

    def need_https(self):
        return False

    def is_inner_api(self):
        return False


