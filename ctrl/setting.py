#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap

@urlmap("/setting")
class Setting(_handler.Base):
    def get(self):
        files = self.request.files
        print files
        self.render()
    post = get
