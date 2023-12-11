# 自定义认证(登录)后端，支持邮箱或手机号登录
# yourapp/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailPhoneBackend(ModelBackend):
    def authenticate(self, request, email=None, phone=None, password=None, **kwargs):
        UserModel = get_user_model()

        if email:
            try:
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                return None

        elif phone:
            try:
                user = UserModel.objects.get(phone=phone)
            except UserModel.DoesNotExist:
                return None

        # 使用Django内置的check_password方法验证密码
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
