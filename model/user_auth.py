#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from hashlib import sha256
from user_mail import user_mail_new, user_id_by_mail
from zsite import zsite_new_user, Zsite

def hash_password(id, password):
    return sha256("%s%s"%(password, id)).digest()

class UserPassword(Model):
    pass

def user_new_session(user_id):
    return

def user_password_new(user_id, password):
    if password is not None:
        o = UserPassword.get_or_create(id=user_id)
        o.password = hash_password(user_id,password)
        o.save()

def user_password_verify(user_id, password):
    p = UserPassword.get(user_id)
    if p is None:
        user_password_new(user_id, password)
        return True
    if p.password == hash_password(user_id,password):
        return True


def user_new_by_mail(mail, password=None):
    user_id = user_id_by_mail(mail)
    if not user_id:
        zsite = zsite_new_user(mail.split("@",1)[0])
        user_id = zsite.id
        user_mail_new(user_id, mail)
        user_password_new(user_id, password)
    return user_id

#mail_id = user_id_by_mail_new(mail, password)

if __name__ == '__main__':
    pass
