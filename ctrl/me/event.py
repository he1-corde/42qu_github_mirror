#!/usr/bin/dev python
# -*- coding: utf-8 -*-
from _handler import LoginBase
from ctrl._urlmap.me import urlmap
from model import reply
from model.cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from model.po import Po, po_rm, po_word_new, po_note_new, STATE_SECRET, STATE_ACTIVE, po_state_set
from model.po_pic import pic_list, pic_list_edit, mc_pic_id_list
from model.zsite import Zsite

from model.event import Event, EventUser, event_feedback_new, CID_EVENT_FEEDBACK, CID_EVENT_INTRODUCTION, CID_EVENT_USER_SATISFACTION, CID_EVENT_USER_GENERAL, CID_EVENT_SUMMARIZED
from zkit.jsdict import JsDict

@urlmap('/event/feedback/(\d+)')
class EventFeedback(LoginBase):
    def get(self, event_id):
        user_id = self.current_user_id
        self.cid = CID_EVENT_FEEDBACK
        event = Event.get(event_id)
        feedback_po = event.feedback_po()
        if event.zsite_id == user_id and not feedback_po:
            self.render(
                '/ctrl/me/po/po.htm',
                cid = self.cid,
                po=JsDict(),
                pic_list=pic_list_edit(user_id, 0),
            )
        else:
            self.redirect(feedback_po.link)

    def post(self, event_id):
        event = Event.get(event_id)
        current_user = self.current_user
        current_user_id = self.current_user_id
        feedback_po = event.feedback_po()
        if event.zsite_id == current_user_id and not feedback_po:
            name = self.get_argument('name', None)
            txt = self.get_argument('txt', None)
            m = event_feedback_new(event_id, current_user_id, name, txt)
            if m:
                event.state = CID_EVENT_SUMMARIZED 
                event.save()
                self.redirect(m.link)




