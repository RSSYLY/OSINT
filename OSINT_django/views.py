import hashlib
import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect
from rest_framework.decorators import api_view

from Utils.Code import *
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# from OSINT_django.models import User
'''
--------------------------------- 用户登录 ---------------------------------
'''


# 登录
@api_view(['POST'])
def login(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Login successful"
    }
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        users = User.objects.filter(username=username)
        if len(users) == 0:  # 懒得改try了，就这样吧
            ret_data["code"] = ITEM_NOT_FOUND_CODE
            ret_data["msg"] = "User not found"
            return HttpResponse(json.dumps(ret_data), content_type="application/json")
        else:
            h1 = hashlib.md5()
            h1.update(password.encode(encoding='utf-8'))
            if users[0].password == h1.hexdigest():
                # 登录成功
                # 将用户id保存到session中，键为user_id，注意该数据存在服务器端
                request.session['user_id'] = users[0].id
                return HttpResponse(json.dumps(ret_data), content_type="application/json")
            else:
                ret_data["code"] = FAIL_CODE
                ret_data["msg"] = "Password error"
                return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 检查用户是否已经登录
@api_view(['GET', ])
def home(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "login success"
    }
    if request.method == 'GET':
        try:
            print(request.COOKIES['sessionid'])
            print(request.session['user_id'])
        except Exception as e:
            print(e)
            ret_data["code"] = FAIL_CODE
            ret_data["msg"] = "login error"
        return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 登出功能，清除session
@api_view(['GET', ])
def logout(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "logout success"
    }
    if request.method == 'GET':
        try:
            request.session.flush()
        except Exception as e:
            print(e)
            ret_data["code"] = FAIL_CODE
            ret_data["msg"] = "logout error"
        response = JsonResponse(ret_data)
        response['Location'] = '/index/'
        return response


# 首页
def index(request):
    return HttpResponse('/index/')  # 这函数的顺序过于混乱了，不好评价，然后这个函数我也不知道是干嘛的，但是写了就不会报错，这下不得不加上了


'''
--------------------------------- 用户注册 ---------------------------------
'''


# 注册
@api_view(['POST', ])
def register(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Register successful"
    }
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if username and password and email:
            # 检查用户名是否已经存在
            if User.objects.filter(username=username).exists():
                ret_data["code"] = FAIL_CODE
                ret_data["msg"] = "Username already exists"
            else:  # 成功，保存用户信息
                h1 = hashlib.md5()
                h1.update(password.encode(encoding='utf-8'))
                hashed_password = h1.hexdigest()
                # 直接保存哈希密码
                user = User.objects.create(username=username, password=hashed_password, email=email)
                user.save()
        else:
            ret_data["code"] = FAIL_CODE
            ret_data["msg"] = "Missing username, password or email"
    return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 在用户注册后，为用户创建token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


'''
--------------------------------- 其他 ---------------------------------
'''


# 获取所有用户
@api_view(['GET', ])
def get_all_users(request):
    users = User.objects.all()
    user_list = list(users.values('username', 'email'))
    return JsonResponse(user_list, safe=False)
