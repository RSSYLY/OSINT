import hashlib
import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from Utils.Code import *
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# from OSINT_django.models import User
'''
--------------------------------- 用户登录 ---------------------------------
'''


# 登录，是否有token认证都可访问
@api_view(['POST'])
@permission_classes((AllowAny, ))
def login(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Login successful"
    }
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
            users = User.objects.filter(username=username)
            if len(users) == 0:
                ret_data["code"] = ITEM_NOT_FOUND_CODE
                ret_data["msg"] = "User not found"
                return HttpResponse(json.dumps(ret_data), content_type="application/json")
            else:
                h1 = hashlib.md5()
                h1.update(password.encode(encoding='utf-8'))
                if users[0].password == h1.hexdigest():
                    # 登录成功
                    # 创建或获取 token
                    token, created = Token.objects.get_or_create(user=users[0])
                    # 将 token、用户 ID 和电子邮件添加到响应数据中
                    ret_data.update({
                        'token': token.key,
                        'user_id': users[0].pk,
                        'email': users[0].email
                    })
                    return HttpResponse(json.dumps(ret_data), content_type="application/json")
                else:
                    ret_data["code"] = FAIL_CODE
                    ret_data["msg"] = "Password error"
                    return HttpResponse(json.dumps(ret_data), content_type="application/json")
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
        return HttpResponse(json.dumps(ret_data), content_type="application/json")

'''
舍弃该方案，将采用前端接到后端返回值为401时自动退出登录
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
'''

'''
--------------------------------- 用户登出 ---------------------------------
'''
'''
舍弃该部分，使用前端登出
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
'''



'''
--------------------------------- 用户注册 ---------------------------------
'''


# 注册
@api_view(['POST', ])
@permission_classes((AllowAny, ))
def register(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Register successful"
    }
    try:
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
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
        return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 在用户注册后，为用户创建token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


'''
--------------------------------- 其他 ---------------------------------
'''


# 获取所有用户，仅登录下可请求
@api_view(['GET', ])
def get_all_users(request):
    users = User.objects.all()
    user_list = list(users.values('username', 'email'))
    return JsonResponse(user_list, safe=False)
