#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache
from hashlib import sha256
from config import SITE_DOMAIN, SITE_DOMAIN_SUFFIX

class Url(Model):
    pass

mc_url_by_id = McCache('UrlById<%s')
mc_id_by_url = McCache('IdByUrl<%s')

@mc_url_by_id('{id}')
def url_by_id(id):
    u = Url.get(id)
    if u is None:
        return ''
    url = u.url
    mc_id_by_url.set(url, u.id)
    return url


def url_or_id(id):
    return url_by_id(id) or id

@mc_id_by_url('{url}')
def _id_by_url(url):
    u = Url.get(url=url)
    if u is None:
        return 0
    return u.id

def id_by_url(url):
    url = url.lower()
    return _id_by_url(url)

def url_new(id, url):
    id = int(id)
    if id_by_url(url):
        return
    u = Url.get_or_create(id=id)
    u.url = url
    u.save()
    mc_id_by_url.set(url, id)
    mc_url_by_id.set(id, url)

NO_URL = set(('god', 'admin', 'review', 'lolicon', 'lolita', 'loli', 'risako', 'lara', 'luna', 'nuva'))
RESERVED_URL = set(('google', 'youdao', 'taobao', 'douban', 'facebook', 'twitter', 'javaeye')) | NO_URL
RE_URL = re.compile(r'^[a-zA-Z0-9\-]*$')

def url_valid_base(url):
    if len(url) < 3:
        return '个性域名至少有3个字符'
    if len(url) > 32:
        return '个性域名最多有32个字符'
    if url in NO_URL:
        return '该网址是我们的保留网址'
    if url.isdigit():
        return '个性域名不能是纯数字'
    if url.startswith('-'):
        return '个性域名不能以-开头'
    if url.endswith('-'):
        return '个性域名不能以-结尾'
    if not RE_URL.match(url):
        return '个性域名格式不正确，请参阅下面说明'
    if id_by_url(url):
        return '该网址已经被占用'

def url_valid(url):
    if len(url) < 5:
        return '个性域名至少有5个字符'
    if url in RESERVED_URL:
        return '该网址是我们的保留网址'
    return url_valid_base(url)

def zsite_by_domain(domain):
    from zsite import Zsite
    if domain.endswith(SITE_DOMAIN_SUFFIX):
        domain = domain[:-len(SITE_DOMAIN_SUFFIX)]
        if domain.isdigit():
            zsite_id = domain
        else:
            zsite_id = id_by_url(domain)
        return Zsite.mc_get(zsite_id)

def link(id):
    return '//%s.%s' % (url_by_id(id) or id, SITE_DOMAIN)

if __name__ == '__main__':
    print id_by_url("i000000")
    print id_by_url("mr-tang")
    print url_by_id(10008333)
