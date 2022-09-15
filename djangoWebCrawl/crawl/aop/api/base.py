# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Created on 2016-12-26

@author: Alibaba Open Platform

"""

import sys
import hmac
import hashlib
import requests
try:
    import simplejson as json
except (ImportError, SyntaxError):
    import json

import aop

PY3 = sys.version_info >= (3,)

# constants
P_OPENAPI = 'openapi'
P_API = 'api'
P_PARAM2 = 'param2'

# system parameters
P_ACCESS_TOKEN = 'access_token'
P_TIMESTAMP = '_aop_timestamp'
P_SIGN = '_aop_signature'

P_ERROR_CODE = 'error_code'
P_ERROR_MESSAGE = 'error_message'
P_EXCEPTION = 'exception'
P_REQUEST_ID = 'request_id'

P_SYS_PARAMS =[P_TIMESTAMP, P_SIGN, P_ACCESS_TOKEN]

def is_sys_param(param_name):
    return param_name in P_SYS_PARAMS

def mix_str(pstr):
    if isinstance(pstr, str):
        return pstr
    if not PY3 and isinstance(pstr, unicode):
        return pstr.encode('utf-8')
    else:
        return str(pstr)


###############################################################################
class FileItem(object):
    def __init__(self, filename=None, content=None):
        """
        Parameters
        ----------
        content : file-like-object(str/bytes/bytearray or an object that has read attribute)
            e.g. f = open('filepath', 'rb') ... fileitem = aop.api.FileItem('filename', f)
            e.g. fileitem = aop.api.FileItem('filename', 'file_content_str')

        """
        self.filename = filename
        self.content = content

class BaseApi(object):
    """"Base class of APIs.

    """

    def raise_aop_error(self, *args):
        _args = ['API: ' + self.get_api_uri()]
        if args:
            _args.extend(args)
        raise aop.AopError(*_args)

    def __init__(self, domain=None):
        """

        Parameters
        ----------
        domain : str
            Remote server domain. e.g. 'gw.open.1688.com' for 1688.

        """
        self.__domain = domain
        if not self.__domain and aop.get_default_server():
            self.__domain = aop.get_default_server()
        self.__httpmethod = "POST"
        default_appinfo = aop.get_default_appinfo()
        #print(default_appinfo)
        if default_appinfo:
            self.__appkey = default_appinfo.appkey
            self.__secret = default_appinfo.secret
        else:
            self.__appkey = ''
            self.__secret = ''

    def sign(self, urlPath, params, secret):
        """Method to generate _aop_signature.

        Parameters
        ----------
        urlPath : str
            param2/version/namespace/name/appkey
        params : dict-like
        secret : str

        References
        ----------
        https://open.1688.com/api/sysSignature.htm

        """
        if not urlPath:
            self.raise_aop_error('sign error: urlPath missing')
        if not secret:
            self.raise_aop_error('sign error: secret missing')
        paramList = []
        if params:
            if not hasattr(params, "items"):
                self.raise_aop_error('sign error: params must be dict-like')
            paramList = [mix_str(k) + mix_str(v) for k, v in params.items()]
            paramList = sorted(paramList)

        msg = bytearray(urlPath.encode('utf-8'))
        for param in paramList:
            msg.extend(bytes(param.encode('utf-8')))

        sha = hmac.new(bytes(secret.encode('utf-8')), None, hashlib.sha1)
        sha.update(msg)
        return sha.hexdigest().upper()

    def set_timestamp(self, timestamp):
        self._aop_timestamp = timestamp

    def set_accesstoken(self, access_token):
        self.access_token = access_token

    def set_appinfo(self, appkey, secret):
        if appkey and secret:
            self.__appkey = appkey

            self.__secret = secret

#################### Methods to implement by subclasses, begin
    def get_api_uri(self):
        """
        Returns
        -------
        str
            version/namespace/name
        """
        return ''

    def need_sign(self):
        """True if _aop_signature is needed"""
        return False

    def need_timestamp(self):
        """True if _aop_timestamp is needed"""
        return False

    def need_auth(self):
        """True if access_token is needed"""
        return False

    def need_https(self):
        """True if to send a https request"""
        return False

    def is_inner_api(self):
        """True if not an open api. Usually false."""
        return False

    def get_multipart_params(self):
        """
        Returns
        -------
        list
            API parameters with type of byte[].
            A multipart request will be sent if not empty.
            e.g. returns ['image'] if the 'image' parameter's type is byte[].
                Then assign it as req.image = aop.api.FileItem('imagename.png', imagecontent)

        """
        return []

    def get_required_params(self):
        """
        Names of required API parameters.
        System parameters(access_token/_aop_timestamp/_aop_signature) excluded.

        An AopError with message 'Required params missing: {"missing_param1_name", ...}'
        will be thrown out if some of the required API parameters are missing before a
        request sent to the remote server.

        """
        return []
#################### Methods to implement by subclass, end

    def __get_url_protocol(self):
        return 'https' if self.need_https() else 'http'

    def _build_sign_url_path(self):
        return '%s/%s/%s' % (P_PARAM2, self.get_api_uri(), self.__appkey)

    def _build_url(self, sign_url_path):
        return '%s://%s/%s/%s' % (self.__get_url_protocol(), self.__domain,
                                  P_API if self.is_inner_api() else P_OPENAPI, sign_url_path)

    def _check_sign(self):
        if self.need_sign():
            if not self.__appkey:
                self.raise_aop_error('AppKey missing')
            if not self.__secret:
                self.raise_aop_error('App secret missing')

    def _check_auth(self, **kwargs):
        if self.need_auth():
            if not kwargs.get(P_ACCESS_TOKEN):
                self.raise_aop_error('access_token missing')

    def _check_required_params(self, **kwargs):
        missing_params = set(self.get_required_params()) - set(kwargs.keys())
        if missing_params:
            self.raise_aop_error('Required params missing: %s' % (str(missing_params)))

    def _gen_timestamp(self, server):
        timestamp_generator = aop.get_timestamp_generator()
        if not timestamp_generator:
            timestamp_generator = aop.get_local_timestamp
        try:
            return timestamp_generator(self.__appkey, self.__secret, server)
        except Exception as e:
            self.raise_aop_error('Failed to generate timestamp. Error: ' + str(e))

    def _check_server(self):
        if not self.__domain:
            if aop.get_default_server():
                self.__domain = aop.get_default_server()
            else:
                self.raise_aop_error('Remote server domain not set')

    def get_response(self, timeout=None, **kwargs):
        self._check_server()

        params = self._get_nonnull_biz_params()
        if kwargs:
            params.update(kwargs)

        if self.need_sign():
            self._check_sign()
        if self.need_auth():
            self._check_auth(**params)
        if self.get_required_params():
            self._check_required_params(**params)
        if self.need_timestamp() and (not params.get(P_TIMESTAMP)):
                params[P_TIMESTAMP] = self._gen_timestamp(self.__domain)

        for multipart_param in self.get_multipart_params():
            params.pop(multipart_param)

        sign_url_path = self._build_sign_url_path()
        if self.need_sign() and (not params.get(P_SIGN)):
            params[P_SIGN] = self.sign(sign_url_path, params, self.__secret)

        url = self._build_url(sign_url_path)

        headers = self._get_request_header()

        files = {}
        if self.get_multipart_params():
            for key in self.get_multipart_params():
                fileitem = getattr(self, key)
                if(fileitem and isinstance(fileitem, FileItem)):
                    files[key] = (fileitem.filename, fileitem.content)
                else:
                    self.raise_aop_error(key + ' not a FileItem')

        resp = self._do_request(url, params, files, headers=headers, timeout=timeout)

        failed = not (resp.status_code >= 200 and resp.status_code < 400)
        ret = resp.text

        try:
            ret = json.loads(ret)
        except Exception as e:
                if failed:
                    self.raise_aop_error('API call error. status_code:%s response:%s' % (str(resp.status_code), str(ret)))
                else:
                    self.raise_aop_error('API call seemed to go ok. But we failed to read the json data. status_code:%s response:%s' % (str(resp.status_code), str(ret)))

        if failed:
            error = aop.ApiError()
            error.api = self.get_api_uri()
            if hasattr(ret, 'get'):
                error.error_code = ret.get(P_ERROR_CODE)
                error.error_message = ret.get(P_ERROR_MESSAGE)
                error.exception = ret.get(P_EXCEPTION)
                error.request_id = ret.get(P_REQUEST_ID)
            raise error

        return ret

    def _do_request(self, url, data=None, files=None, **kwargs):
        try:
            if files:
                return requests.post(url, data=data, files=files, **kwargs)
            else:
                return requests.post(url, data=data, **kwargs)
        except requests.RequestException as e:
                self.raise_aop_error(str(e))

    def _get_request_header(self):
        return {
                 'Cache-Control': 'no-cache',
                 'Connection': 'Keep-Alive',
                 'User-Agent':'Ocean-SDK-Client'
        }

    def _is_nonnull_biz_param(self, param_name, param_value):
        if is_sys_param(param_name):
            return True
        return (not param_name.startswith("__")) \
            and (not param_name.startswith("_BaseApi__")) \
            and param_value

    def _get_nonnull_biz_params(self):
        biz_params = {}
        for key, value in self.__dict__.items():
            if self._is_nonnull_biz_param(key, value):
                biz_params[key] = value
        return biz_params

