#coding:utf-8
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from zkit.errtip import Errtip
from model.user_auth import user_password_verify, UserPassword, user_password_new
from model.user_info import user_info_new, UserInfo as _UserInfo

@urlmap("/j/auth/guide/1")
class AuthGuide1(JLoginBase):
    def post(self):

        current_user = self.current_user
        current_user_id = current_user.id
        result = {}
        error = {}

        
        name = self.get_argument('name', None)
        if not name:
            error['name'] = "请输入姓名"

        sex = None
        info = _UserInfo.mc_get(current_user_id)
        if not (info and info.sex):
            sex = self.get_argument('sex', '0')
            if not(sex and int(sex) in (1, 2)):
                error['sex'] = '请选择性别'

        password = None
        if not UserPassword.get(current_user_id):
            password = self.get_argument('password', None)
            if not password:
                error['password'] = '请输入密码'

        if not error:
            if password:
                user_password_new(current_user_id, password)

            if sex:
                user_info_new(current_user_id, sex=sex)

            current_user.name = name
            current_user.save()
        else:
            result['error'] = error

        self.finish(result)
 
@urlmap("/j/auth/guide/2")
class AuthGuide2(JLoginBase):
    def post(self):
        result = {}
        self.finish(result)


@urlmap("/j/auth/guide/3")
class AuthGuide3(JLoginBase):
    def post(self):
        result = {}
        self.finish(result)

