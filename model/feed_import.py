#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from _db import Model, McModel
from po import po_note_new
from douban import DoubanUser, douban_feed_to_review_iter, douban_user_by_feed_id , title_normal
from model.txt_img_fetch import txt_img_fetch
from kv import Kv
from url_short import url_short_id
from site_sync import site_sync_new
from rec_read import  rec_read_new
from po_by_tag import zsite_tag_po_new_by_name, po_tag_id_list_new
from part_time_job import part_time_job_new
from config.privilege import PRIVILEGE_FEED_IMPORT


FEED_IMPORT_STATE_RM = 0
FEED_IMPORT_STATE_INIT = 10

FEED_IMPORT_STATE_REVIEWED = 20
FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR = 30
FEED_IMPORT_STATE_REVIEWED_SYNC = 40
FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC = 50

FEED_IMPORT_STATE_POED = 60 

DOUBAN_ZSITE_ID = 10216239

FEED_IMPORT_CID_DICT = {
        DOUBAN_ZSITE_ID : 1, #douban
        }

class PoMeta(McModel):
    pass

class FeedImport(Model):
    pass

class PoMetaUser(McModel):
    @property
    def link(self):
        if self.cid == DOUBAN_ZSITE_ID:
            return 'http://www.douban.com/people/%s'%self.url

def user_url_by_po_meta_user_id(id):
    user = PoMetaUser.mc_get(id)
    if user:
        if user.cid == DOUBAN_ZSITE_ID:
            return 'http://www.douban.com/people/%s'%user_id.url

def user_by_feed_id_zsite_id(feed_id, zsite_id):
    if zsite_id == DOUBAN_ZSITE_ID:
        return douban_user_by_feed_id(feed_id)

def feed_next():
    fdlist = FeedImport.where(state=FEED_IMPORT_STATE_INIT)[1:2]
    if fdlist:
        return fdlist[0]

def feed_import_rm(id, current_user_id):
    part_time_job_new(PRIVILEGE_FEED_IMPORT, id, current_user_id)
    feed_state_set(id, FEED_IMPORT_STATE_RM)


def feed_state_set(id, state):
    feed = FeedImport.get(id)
    if feed:
        feed.state = state
        feed.save()

def zsite_id_by_douban_user_id(douban_user):
    #TODO: get zsite_user_id
    return 0
    zsite_id = 0
    if douban_user:
        douban_username = douban_user.name
        zsite_id = 10001518
    return zsite_id

def feed2po_new():
    from zweb.orm import ormiter
    for feed in ormiter(
            FeedImport,
            'state>%s and state<%s'%(
                FEED_IMPORT_STATE_INIT,
                FEED_IMPORT_STATE_POED
            )
        ):
        txt = txt_img_fetch(feed.txt)
        feed_user = user_by_feed_id_zsite_id(feed.rid, feed.zsite_id)
        user_id = zsite_id_by_douban_user_id(feed_user)

        zsite_id = feed.zsite_id

        is_without_author = ((feed.state == FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC) or (feed.state == FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR))

        if is_without_author:
            user_id = 0
            zsite_id = 0

        title = title_normal(feed.title)
        po = po_note_new(user_id, title, txt, zsite_id=zsite_id)

        if po:
            if not feed_user:
                feed_user_id = 0
            else:
                user = PoMetaUser.get_or_create(name = feed_user.name, cid = zsite_id)
                user.url = feed_user.id

                user.save()

                feed_user_id = user.id

            record = PoMeta.get_or_create(id = po.id)
            record.user_id = feed_user_id
            record.url_id = url_short_id(feed.url)

            record.save()

            if not is_without_author:
                po.rid = record.id
                po.save()

            if feed.state >= FEED_IMPORT_STATE_REVIEWED_SYNC:
                site_sync_new(po.id)

            feed.state = FEED_IMPORT_STATE_POED
            feed.save()

            po_tag_id_list_new(po, feed.tag_id_list.split())

def feed_review(id,  title, txt, tag_id_list, current_user_id, author_rm=False, sync=False):
    feed = FeedImport.get(id)
    if feed and feed.state==FEED_IMPORT_STATE_INIT :
        if author_rm:
            if sync:
                feed.state = FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC
            else:
                feed.state = FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR
        else:
            if sync:
                feed.state = FEED_IMPORT_STATE_REVIEWED_SYNC
            else:
                feed.state = FEED_IMPORT_STATE_REVIEWED

        feed.title = title
        feed.txt = txt
        feed.tag_id_list = tag_id_list
        
        part_time_job_new(PRIVILEGE_FEED_IMPORT, feed.id, current_user_id)

        feed.save()


if __name__ == '__main__':
    pass
    #feed_import_by_douban_feed()
    #print FeedImport.where(state = FEED_IMPORT_STATE_INIT)
    #feed2po_new()
    #from zweb.orm import ormiter
    #for i in ormiter(FeedImport):
    #    i.txt = i.txt.replace("豆友","网友").replace("豆油","私信").replace("豆邮","私信")
    #    i.tag_id_list = ""
    #    print i.id, i.tag_id_list
    #    i.save()
    print FeedImport.where(state=FEED_IMPORT_STATE_INIT)[:2]
    print FeedImport.get(state = FEED_IMPORT_STATE_INIT)