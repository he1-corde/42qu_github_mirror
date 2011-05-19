#!/usr/bin/env python
#coding:utf-8
import init_env
from zweb.orm import ormiter
from model.zsite import Zsite

def host_line(host):
    l = ["""192.168.1.106 %s p.%s s.%s god.%s"""%(
        host, host, host, host
    )]
    for i in ormiter(Zsite):
        print i.link
    return "".join(l)

if __name__ == "__main__":
    for name in ("zuroc.me","zjd.me","yup.me"):
        print host_line(name)
