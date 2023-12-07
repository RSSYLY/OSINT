from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        # user变量局部定义
        user = None
        # 获取前端发送的 JSON 数据
        data = json.loads(request.body.decode('utf-8'))

        # 提取登录信息
        login_type = data.get('loginType')

        # 根据登录类型验证用户
        if login_type == 'email':
            email = data.get('email')
            password = data.get('password')
            # 此处通过自定义后端实现邮箱、电话登录
            user = authenticate(request, email=email, password=password)
        elif login_type == 'phone':
            phone = data.get('phone')
            password = data.get('password')
            user = authenticate(request, phone=phone, password=password)

        if user is not None:
            # 登录成功
            login(request, user)
            # 生成或获取用户的Token,token存放于 authtoken_token表
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'message': '登录成功', 'data': {'taken': token.key}, 'error': 'null'})
        else:
            # 登录失败
            return JsonResponse({'message': '账号或密码错误，请重试'}, status=401)

    # 如果不是 POST 请求，返回错误信息
    return JsonResponse({'message': '非法请求'}, status=400)


def register_view(request):
    return JsonResponse({'注册'})


def forgot_password_view(request):
    return JsonResponse({'忘记密码'})
