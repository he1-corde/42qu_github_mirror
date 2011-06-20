#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from os import urandom
from user_mail import user_mail_new, user_id_by_mail
from zsite import zsite_new_user, Zsite
from txt import txt_property, txt_new
from gid import gid
from uuid import uuid4
from _db import McCache
from urllib import urlencode
from hashlib import sha256
import binascii
from operator import itemgetter
from config import SITE_DOMAIN
from user_session import password_encode

API_URL = 'http://api.%s'%SITE_DOMAIN

mc_api_serect = McCache('ApiSerect:%s')
mc_api_session = McCache('ApiSession:%s')

class ApiSession(Model):
    pass

class ApiClient(Model):
    txt = txt_property

    @property
    def hex_serect(self):
        return binascii.hexlify(self.serect)

def api_client_new(user_id, name, txt):
    serect = uuid4().bytes
    id = gid()
    api_client = ApiClient(id, user_id=user_id, serect=serect)

    api_client.name = name
    txt_new(api_client.id, txt)
    api_client.save()
    hex_serect = binascii.hexlify(serect)
    mc_api_serect.set(id, hex_serect)
    return api_client

@mc_api_serect('{id}')
def api_serect(id):
    api = ApiClient.get(id)
    if api:
        return binascii.hexlify(client.serect)
    return 0

@mc_api_session('{client_id}_{user_id}')
def api_session(client_id, user_id):
    u = ApiSession.get(user_id=user_id, client_id=client_id)
    if u is not None:
        return u.value or False
    return False

def api_session_new(client_id, user_id):
    value = api_session(user_id, client_id)
    if not value:
        ApiSession.get_or_create(user_id=user_id, client_id=client_id)
        session.value = value = urandom(12)
        session.save()
        mc_api_session.set('%s_%s'%(client_id, user_id), session.value)
    return password_encode(user_id, value)

#生成的url
def client_url_encode(arguments):
    items = arguments.items()
    items.sort(key=itemgetter(0))
    return urlencode(items)

def _api_sign(arguments, serect):
    _url = client_url_encode(arguments)
    url = '&'.join((_url, 'client_serect=%s'%serect))
    return sha256(url).hexdigest(), _url

#生成签名
def api_sign(arguments, serect):
    return _api_sign(arguments, serect)[0]

#服务器效验URL
def api_sign_verify(arguments):
    client_id = arguments['client_id']
    sign = arguments['sign']
    client_secret = api_serect(client_id)
    del arguments['sign']
    sign2 = api_sign(arguments, client_secret)
    if sign == sign2:
        return True

#生成已经签名了的参数
def api_sign_arguments(arguments, serect):
    sign , url = _api_sign(arguments, serect)
    return '%s&sign=%s'%(url, sign)

######## 以下为客户端生成URL的演示部分 #########

def api_login_token(user_id, mail, password):
    mail = mail.strip().lower()
    password = password.strip()
    hexdigest = sha256(password+str(user_id)).hexdigest()
    return sha256(mail+hexdigest).hexdigest()

def api_login_url(
    client_id, serect,
    user_id, mail, password
):
    arguments = dict(
        user_id=user_id,
        client_id=client_id,
        mail=mail,
        token=api_login_token(user_id, mail, password)
    )
    url = api_sign_arguments(arguments, serect)
    return '%s/user/auth/login?%s'%(API_URL, url)

if __name__ == '__main__':
    api_client = ApiClient.get(73)
    serect = api_client.hex_serect
    print 'client_id', api_client.id
    print 'client_serect', serect
    arguments = {
        'client_id': api_client.id,
        'test':'abc',
        'test2':'123'
    }
    print 'arguments', arguments
    sign = api_sign(arguments, serect)
    print 'sign', sign
    arguments['sign'] = sign
    api_sign_verify(arguments)




    client_id = 73
    serect = 'beafcff6034e4b26b914241235e66da4'
    user_id = 74
    mail = 'test@42qu.com'
    password = '123456'
    print api_login_url(
        client_id, serect, user_id, mail, password
    )

    print api_session_new(user_id, client_id)
