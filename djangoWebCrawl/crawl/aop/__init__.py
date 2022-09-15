# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Created on 2016-12-26

@author: Alibaba Open Platform

"""

import time
import datetime

from .api import GetServerTimestampRequest

class AopError(Exception):
    """
    1. Failed before sending a request.
        e.g. Some of the required API parameters missing.
    2. Failed to parse the returned results.

    """
    pass

class ApiError(Exception):
    """
    The remote server returned error and the error messages were successfully recognized.

    Attributes
    ----------
    api : str
    error_code : str
    error_message : str
    exception : str
    request_id : str

    """
    def __init__(self):
        self.api = ''
        self.error_code = ''
        self.error_message = ''
        self.exception = ''
        self.request_id = ''

    def __str__(self, *args, **kwargs):
        return 'ApiError [api=%s; error_code=%s; error_message=%s; exception=%s; request_id=%s]' % \
            (self.api, self.error_code, self.error_message, self.exception, self.request_id)

class AppInfo(object):
    def __init__(self, appkey, secret):
        self.appkey = appkey

        self.secret = secret

def get_default_appinfo():
    pass

def set_default_appinfo(appkey, secret):
    """Set default appkey and secret.

    Parameters
    ----------
    appkey : int
    secret : str

    Notes
    -----
    Secret will be saved in plain text in memory.

    """
    global get_default_appinfo
    get_default_appinfo = lambda : AppInfo(appkey, secret)

def get_default_server():
    pass

def set_default_server(remote_server):
    if remote_server:
        default_server = remote_server
        global get_default_server
        get_default_server = lambda: default_server

def get_timestamp_diff(appkey, secret, server):
    """
    Returns
    -------
    int
        timestamp difference between the server and the local.

    Raises
    ------
    AopError
        First calls API '1/system/currentTimeMillis'. So it may fail due to different reasons.

    """
    return get_server_timestamp(appkey, secret, server) - get_local_timestamp()

def get_server_timestamp(appkey, secret, server):
    """
    Returns
    -------
    int
        Milliseconds since midnight, January 1, 1970 UTC. e.g. 1484033752883

    Raises
    ------
    AopError
        Actually calls API '1/system/currentTimeMillis'. So it may fail due to different reasons.

    """
    req = GetServerTimestampRequest(server)
    req.set_appinfo(appkey, secret)
    try:
        return req.get_response()
    except Exception as e:
        raise AopError('Failed to get server timestamp from %s. Reason: %s' % (server, str(e)))

def get_local_timestamp(appkey=None, secret=None, server=None):
     return int(time.time() * 1000)


def get_timestamp_generator():
    return get_local_timestamp

def set_timestamp_generator(timestamp_generator):
    """Set timestamp generator.

    Timestamp is milliseconds since midnight, January 1, 1970 UTC and needed by some APIs
    due to security concerns.

    Timestamp generator is a function taking three arguments: appkey, secret, server domain.

    Generally, there are three policy to generate the timestamp.
    1. Use the local time every time.
        This is the default policy.
        You should first check the time difference between your local machine and the server.
    2. Use the server time every time. NOT RECOMMENDED!
        Just call aop.set_timestamp_generator(aop.get_server_timestamp)
        But remember that there is a call limit for the the API per 10-minutes.
    3. Get the timestamp by the formula: local_timestamp + timestamp_diff.
        "timestamp_diff" is the time difference between the server and the local that saved
        somewhere and periodically synchronized by calling aop.get_timestamp_diff().
        e.g.
            1> periodically synchronize timestamp_diff:
                timestamp_diff = aop.get_timestamp_diff(appkey, secret, server)
            2> aop.set_timestamp_generator(lambda appkey, secret, server: timestamp_diff + aop.get_local_timestamp())

    Parameters
    ----------
        timestamp_generator : callable taking three arguments: appkey, secret, server domain.

    """
    if timestamp_generator:
        default_timestamp_generator = timestamp_generator
        global get_timestamp_generator
        get_timestamp_generator = lambda : default_timestamp_generator

