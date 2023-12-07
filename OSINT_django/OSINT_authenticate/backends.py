# 自定义认证后端，支持邮箱或手机号登录
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q  # Q用于构造复杂的查询条件，比如or查询，not查询等，可以使用 & | ~ 等操作符进行连接，这些操作符被 Q 重载过，所以可以直接使用。


class MultiFieldBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # 通过 Q 对象，实现了 email 或 phone 字段的或查询
            user = UserModel.objects.get(Q(email=username) | Q(phone=username))
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
