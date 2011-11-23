#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM
from mail import rendermail
from model.days import today_seconds
from model.zsite_member import zsite_member_new, ZSITE_MEMBER_STATE_ACTIVE

COM_APPLY_STATE_APPLY_MAILED = 30
COM_APPLY_STATE_APPLY = 20
COM_APPLY_STATE_APPLY_ACCEPT = 10
COM_APPLY_STATE_DEL = 0

mc_com_apply_id_list = McCacheA("ComApplyIdList:%s")

class ComApply(McModel):
    pass

@mc_com_apply_id_list("{id}")
def com_apply_id_list(id):
    return ComApply.where(com_id=id).where("state>=%s"%COM_APPLY_STATE_APPLY).col_list()


def com_apply_list(id):
    return ComApply.mc_get_list(com_apply_id_list(id))

def com_apply_get(com_id,user_id,state=COM_APPLY_STATE_APPLY):
    c = ComApply.get(com_id=com_id,user_id=user_id)
    if c: 
        return c.state >= COM_APPLY_STATE_APPLY 

def com_apply_new(user_id,com_id):
    ca = ComApply.get_or_create(com_id=com_id,user_id=user_id)
    ca.state = COM_APPLY_STATE_APPLY
    ca.create_time = today_seconds()
    ca.save()

    mc_com_apply_id_list.delete(com_id)

    #admin_id_list = admin_id_list_by_zsite_id(com_id)
    #rendermail(
    #        '/mail/notice/com_apply.txt',
    #        mail_by_user_id(user_id),
    #        user = Zsite.mc_get(user_id),
    #        com = Zsite.mc_get(com_id)
    #        )

def com_apply_rm(user_id,com_id,admin_id):
    ca = ComApply.get(user_id=user_id,com_id=com_id)
    if ca:
        ca.state = COM_APPLY_STATE_DEL
        ca.admin_id = admin_id
        ca.create_time = today_seconds()
        ca.save()

def com_apply_accept(user_id,com_id,admin_id):
    zsite_member_new(com_id, user_id, ZSITE_MEMBER_STATE_ACTIVE)

    ca = ComApply.get_or_create(user_id=user_id,com_id=com_id,)
    ca.admin_id=admin_id
    ca.create_time = today_seconds()
    ca.state = COM_APPLY_STATE_APPLY_ACCEPT
    ca.save()
    


