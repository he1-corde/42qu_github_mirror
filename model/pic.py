#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache
from time import time
from fs import fs_set_jpg, fs_url_jpg
from cid import CID_ICO, CID_ICO96, CID_PO_PIC, CID_PIC

class Pic(Model):
    def __getattr__(self, name):
        if name.startswith('ico'):
            size = name[3:]
            if size.isdigit():
                return fs_url_jpg(size, self.id)

def pic_new(cid, user_id):
    p = Pic(
        cid=cid,
        user_id=user_id,
        create_time=int(time()),
    ).save()
    return p.id

def pic_save(pic_id, pic):
    fs_set_jpg('0', pic_id, pic)

def pic_need_review(cid):
    qs = Pic.where(cid=cid, state=0, admin_id=0)[:1]
    return len(qs)

def _pic_list_to_review_by_cid(cid, start_id, limit):
    return Pic.where(cid=cid, state=0, admin_id=0).where('id>%s' % start_id).order_by('id')[:limit]

def pic_ico_to_review_iter(limit):
    from ico import ico
    count = 0
    start_id = 0
    while True:
        li = _pic_list_to_review_by_cid(CID_ICO, start_id, limit)
        for i in li:
            id = i.id
            user_id = i.user_id
            user_pic_id = ico.get(user_id)
            if id == user_pic_id:
                count += 1
                yield i
                if count == limit:
                    return
            elif not user_pic_id:
                ico.set(user_id, id)
            else:
                i.state = 1
                i.save()
        if len(li) < limit:
            return
        else:
            start_id = id

def pic_ico_to_review(limit):
    return list(pic_ico_to_review_iter(limit))

def pic_to_review_count_by_cid(cid):
    return Pic.where(cid=cid, state=0, admin_id=0).count()

def pic_list_to_review_by_cid(cid, limit):
    if cid == CID_ICO:
        return pic_ico_to_review(limit)
    return _pic_list_to_review_by_cid(cid, limit)

def pic_list_reviewed_by_cid_state(cid, state, limit, offset):
    return Pic.where(cid=cid, state=state).where('admin_id>0').order_by('id desc')[offset: offset + limit]

def pic_reviewed_count_by_cid(cid, state):
    return Pic.where(cid=cid, state=state).where('admin_id>0').count()

def pic_yes(id, admin_id):
    p = Pic.mc_get(id)
    if p:
        p.admin_id = admin_id
        p.state = 1
        p.save()

def pic_no(id, admin_id):
    p = Pic.mc_get(id)
    if p:
        p.admin_id = admin_id
        p.state = 0
        p.save()

if __name__ == '__main__':
    print pic_list_to_review_by_cid(31, 2)
