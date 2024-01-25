import hashlib
import json
import random
import string

from django.contrib.auth.models import User
from django.core.cache import cache
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
@permission_classes((AllowAny,))
def login(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Login successful"
    }
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            login_type = data.get('type')
            username_or_email = data.get('username_or_email')
            password = data.get('password')
            if login_type == 'username':
                users = User.objects.filter(username=username_or_email)
            elif login_type == 'email':
                users = User.objects.filter(email=username_or_email)
            else:
                ret_data["code"] = FAIL_CODE
                ret_data["msg"] = "Invalid login type"
                return HttpResponse(json.dumps(ret_data), content_type="application/json")
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
                    # 将 token、用户 ID 和电子邮件等添加到响应数据中
                    ret_data.update({
                        'username': users[0].username,
                        'id': users[0].pk,
                        'email': users[0].email,
                        'token': token.key,
                        'is_superuser': users[0].is_superuser,
                        'is_staff': users[0].is_staff,
                        'is_active': users[0].is_active,
                        'date_joined': users[0].date_joined.strftime('%Y-%m-%d %H:%M:%S') if users[
                            0].date_joined else None,
                        'last_login': users[0].last_login.strftime('%Y-%m-%d %H:%M:%S') if users[
                            0].last_login else None,
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
--------------------------------- 用户注册 ---------------------------------
'''


# 注册验证码
@api_view(['POST', ])
@permission_classes((AllowAny,))
def register_sendcode(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Register-code has sent successfully"
    }
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        if email:
            # 检查邮箱是否已经存在
            if User.objects.filter(email=email).exists():
                ret_data["code"] = FAIL_CODE
                ret_data["msg"] = "Email already exists"
            else:  # 成功，发送验证码
                # 生成6位验证码
                code = ''.join(random.sample(string.digits, 6))
                # 发送邮件
                print("验证码为：" + code)
                # 将验证码存储在缓存中，设置过期时间为5分钟
                cache.set('res_ver' + email, code, 60 * 5)
        else:
            ret_data["code"] = FAIL_CODE
            ret_data["msg"] = "Missing email"
        return HttpResponse(json.dumps(ret_data), content_type="application/json")
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
        return HttpResponse(json.dumps(ret_data), content_type="application/json")


# 注册
@api_view(['POST', ])
@permission_classes((AllowAny,))
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
            verification_code = data.get('verification_code')
            if username and password and email and verification_code:
                if verification_code != cache.get("res_ver" + email):  # 验证码错误
                    ret_data["code"] = FAIL_CODE
                    print(verification_code, cache.get("res_ver" + email))
                    ret_data["msg"] = "Verification code does not match"

                elif User.objects.filter(username=username).exists():  # 用户名已存在
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
@permission_classes((AllowAny,))
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


'''
--------------------------------- 找回密码 ---------------------------------
'''


@api_view(['POST', ])
@permission_classes((AllowAny,))
def find_password_sendcode(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Verification code has sent successfully"
    }
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('target')
        if email:
            # 检查邮箱是否已经存在
            if not User.objects.filter(email=email).exists():
                ret_data["code"] = FAIL_CODE
                ret_data["msg"] = "Email does not exist"
            else:  # 成功，发送验证码
                # 生成6位验证码
                code = ''.join(random.sample(string.digits, 6))
                # 发送邮件
                print("验证码为：" + code)
                # 将验证码存储在缓存中，设置过期时间为5分钟
                cache.set('find_pass_ver' + email, code, 60 * 5)
        else:
            ret_data["code"] = FAIL_CODE
            ret_data["msg"] = "Missing email"
        return HttpResponse(json.dumps(ret_data), content_type="application/json")
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
        return HttpResponse(json.dumps(ret_data), content_type="application/json")


@api_view(['POST', ])
@permission_classes((AllowAny,))
def find_password(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Password reset successful"
    }
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('target')
            password = data.get('password')
            verification_code = data.get('verification_code')
            if email and password and verification_code:
                if verification_code != cache.get("find_pass_ver" + email):  # 验证码错误
                    ret_data["code"] = FAIL_CODE
                    print(verification_code, cache.get("find_pass_ver" + email))
                    ret_data["msg"] = "Verification code does not match"
                else:  # 成功，保存用户信息
                    h1 = hashlib.md5()
                    h1.update(password.encode(encoding='utf-8'))
                    hashed_password = h1.hexdigest()
                    # 直接保存哈希密码
                    user = User.objects.get(email=email)
                    user.password = hashed_password
                    user.save()
            else:
                ret_data["code"] = FAIL_CODE
                ret_data["msg"] = "Missing email or password"
        return HttpResponse(json.dumps(ret_data), content_type="application/json")
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
        return HttpResponse(json.dumps(ret_data), content_type="application/json")

'''
--------------------------------- 修改密码 ---------------------------------
'''
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def change_password(request):
    ret_data = {
        "code": SUCCESS_CODE,
        "msg": "Password reset successful"
    }
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            old_password = data.get('old_password')
            new_password = data.get('new_password')
            if old_password and new_password:
                h1 = hashlib.md5()
                h1.update(old_password.encode(encoding='utf-8'))
                hashed_old_password = h1.hexdigest()
                if hashed_old_password != request.user.password:  # 旧密码错误
                    ret_data["code"] = FAIL_CODE
                    ret_data["msg"] = "Old password error"
                else:  # 成功，保存用户信息
                    h2 = hashlib.md5()
                    h2.update(new_password.encode(encoding='utf-8'))
                    hashed_new_password = h2.hexdigest()
                    # 直接保存哈希密码
                    user = User.objects.get(username=request.user.username)
                    user.password = hashed_new_password
                    user.save()
            else:
                ret_data["code"] = FAIL_CODE
                ret_data["msg"] = "Missing old password or new password"
        return HttpResponse(json.dumps(ret_data), content_type="application/json")
    except Exception as e:
        ret_data["code"] = SERVER_FAIL_CODE
        ret_data["msg"] = str(e)
        return HttpResponse(json.dumps(ret_data), content_type="application/json")



'''
--------------------------------- 其他 ---------------------------------
'''


# 获取所有用户，仅登录下可请求
@api_view(['GET', ])
def get_all_users(request):
    users = User.objects.all()
    user_list = list(users.values('username', 'email'))
    return JsonResponse(user_list, safe=False)
