#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import McCache, McNum
from cid import CID_EVENT
from po import Po, po_new, po_word_new, po_note_new, po_rm, po_cid_set
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get
from zkit.time_format import time_title
from zsite import Zsite
from model.cid import CID_EVENT, CID_EVENT_FEEDBACK
from model.pic import pic_new_save , fs_url_jpg , fs_set_jpg
from zkit.pic import pic_fit
from rank import rank_po_id_list
from event import EVENT_CID, EVENT_CID_CN, EventJoiner, event_joiner_get, EVENT_JOIN_STATE_FEEDBACK_NORMAL , EVENT_JOIN_STATE_FEEDBACK_GOOD, mc_event_joiner_feedback_normal_id_list, event_joiner_feedback_normal_id_list 

mc_event_feedback_id_get = McCache('EventFeedBackGet.%s')

@mc_event_feedback_id_get("{user_id}_{event_id}")
def event_feedback_id_get(user_id, event_id):
    for i in Po.where(user_id=user_id, rid=event_id).where(
        cid = CID_EVENT_FEEDBACK
    ).where('state>%s', STATE_DEL).col_list(1, 0):
        return i
    return 0


def po_event_pic_new(zsite_id, pic):
    pic_id = pic_new_save(CID_EVENT, zsite_id, pic)
    pic162 = pic_fit(pic, 162)
    fs_set_jpg(162, pic_id, pic162)
    return pic_id


def po_event_feedback_new(user_id, name, txt, good, event_id, event_user_id):
    if not name and not txt:
        return

    id = event_feedback_id_get(user_id, event_id)

    if id:
        m = Po.mc_get(id)
    else:
        m = po_new(CID_EVENT_FEEDBACK, user_id, name, STATE_ACTIVE, event_id)
        id = m.id
        mc_event_feedback_id_get.set('%s_%s' % (user_id, event_id), id)
        m.feed_new()

        from buzz import buzz_event_feedback_new , mq_buzz_event_feedback_owner_new
        
        if user_id!=event_user_id:
            rank_new(m, event_id, CID_EVENT_FEEDBACK)
            buzz_event_feedback_new(user_id, id, event_user_id)
        else:
            mq_buzz_event_feedback_owner_new(user_id, id, event_user_id)

        event_joiner_state_is_good(user_id, event_id, good)
    return m


def event_joiner_state_is_good(user_id, event_id, good):
    event_joiner_state_set(
        user_id, 
        event_id, 
        EVENT_JOIN_STATE_FEEDBACK_GOOD if good else EVENT_JOIN_STATE_FEEDBACK_NORMAL
    )
    

def event_joiner_state_set(user_id, event_id, to_state):
    event_joiner = event_joiner_get(event_id, user_id)
    from_state = event_joiner.state

    if from_state == to_state:
        return

    event_joiner.state = to_state
    event_joiner.save()
    mc_event_joiner_feedback_normal_id_list.delete(event_id) 

def po_event_feedback_rm(user_id, event_id):
    event_joiner_state_set(user_id, event_id, EVENT_JOIN_STATE_END)

def po_event_feedback_list(event_id):
    ids = rank_po_id_list(event_id, CID_EVENT_FEEDBACK, 'confidence')
    
    li = Po.mc_get_list(ids)
    Zsite.mc_bind(li, 'user', 'user_id')

    return li


def po_event_feedback_group(event_id):
    li = po_event_feedback_list(event_id)
    id_set = set(event_joiner_feedback_normal_id_list(event_id))

    good = []
    normal = []

    for i in li:
        if i.user_id in id_set:
            normal.append(i)  
        else:
            good.append(i)

    return good, normal



if __name__ == '__main__':
    print po_event_feedback_group(10047367)


