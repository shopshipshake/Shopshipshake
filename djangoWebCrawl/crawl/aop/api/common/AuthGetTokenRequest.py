# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Created on 2016-12-26

@author: Alibaba Open Platform

"""

from aop.api.base import BaseApi

class AuthGetTokenRequest(BaseApi):
    """
    References
    ----------
    https://open.1688.com/api/sysAuth.htm

    """
    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)

    def get_api_uri(self):
        return '1/system.oauth2/getToken'

    def need_sign(self):
        return False

    def need_timestamp(self):
        return False

    def need_auth(self):
        return False

    def need_https(self):
        return True

    def get_multipart_params(self):
        return []

    def get_required_params(self):
        return []

    def is_inner_api(self):
        return False
