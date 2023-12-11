from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import json
import random
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render

from OSINT_authenticate.models import CustomUser


# Create your views here.

# 登录
def login_view(request):
    if request.method == 'POST':
        # user变量局部定义
        user = None
        # 获取前端发送的 JSON 数据
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        # 提取登录类型
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
            return JsonResponse({
                'message': '登录成功',
                'data': {'token': token.key,
                         'id': user.id,
                         'username': user.username,
                         'email': user.email,
                         'phone': user.phone,
                         'is_superuser': user.is_superuser,
                         'is_staff': user.is_staff,
                         'is_active': user.is_active
                         },
                'error': 0})
        else:
            # 登录失败
            return JsonResponse({
                'message': '邮箱、手机或密码错误',
                'data': {
                },
                'error': 1})

    # 如果不是 POST 请求，返回错误信息
    return JsonResponse({'message': '非法请求'}, status=400)


@csrf_exempt
@require_POST
def register_send_verification_code(request):
    # 注册用户时发送验证码
    try:
        data = json.loads(request.body)
        email = data.get('email')
        if email:
            # 判断该用户是否已经注册（使用邮箱判断）
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({'message': '该邮箱已经注册', 'error': 1})
            # Generate a random 6-digit verification code
            verification_code = str(random.randint(100000, 999999))

            # Store the email and verification code in cache
            # 如果同一用户在缓存结束之前请求发送验证码多次，后端会以最后一次请求为准。每次发送验证码请求时，都会更新相应邮箱的缓存键对应的验证码，因此只有最后一次的验证码会在缓存中存储。之前的验证码会被新的验证码覆盖。
            cache_key = f'reg_verification_code_{email}'
            cache.set(cache_key, verification_code, timeout=300)  # Set a timeout, e.g., 5 minutes

            # Print the verification code to the console
            print(f"Reg_Verification Code for {email}: {verification_code}")

            return JsonResponse({'message': '验证码发送成功', 'error': 0})
        else:
            return JsonResponse({'message': '缺少邮箱参数', 'error': 1})
    except Exception as e:
        return JsonResponse({'message': str(e), 'error': 1})


@csrf_exempt
@require_POST
def register_user(request):
    # 注册用户
    try:
        data = json.loads(request.body)
        email = data.get('email')
        verification_code = data.get('verificationCode')
        password = data.get('password')
        phone = data.get('phone')

        # Validate email and verification code
        cache_key = f'reg_verification_code_{email}'
        stored_verification_code = cache.get(cache_key)

        if verification_code == stored_verification_code:
            # Verification successful, create user (you may need to customize this part)
            # Here, I'm assuming you have a custom user model with an email field

            # 判断手机号是否被使用，需要排除手机号是空的情况
            if phone and CustomUser.objects.filter(phone=phone).exists():
                return JsonResponse({'message': '该手机号已经被使用', 'error': 1})

            CustomUser.objects.create_user(username=email, email=email, password=password, phone=phone)
            # 删除验证码缓存
            cache.delete(cache_key)
            return JsonResponse({'message': '注册成功，请手动登录', 'error': 0})
        else:
            return JsonResponse({'message': '验证码错误', 'error': 1})
    except Exception as e:
        return JsonResponse({'message': '内部错误' + str(e), 'error': 1})


@csrf_exempt
@require_POST
def forgot_password_send_verification_code(request):
    # 忘记密码时发送验证码
    try:
        data = json.loads(request.body)
        target = data.get('target')
        if target:
            # Generate a random 6-digit verification code
            verification_code = str(random.randint(100000, 999999))

            # 如果使用邮箱找回密码
            if data.get('type') == 'email':
                # 先寻找该邮箱是否注册
                if not CustomUser.objects.filter(email=target).exists():
                    return JsonResponse({'message': '该邮箱未注册', 'error': 1})
                # 再生成验证码
                cache_key = f'forgot_verification_code_{target}'
                cache.set(cache_key, verification_code, timeout=300)  # Set a timeout, e.g., 5 minutes

                # Print the verification code to the console
                print(f"向 {target} 这个邮箱发送了验证码: {verification_code}")
            # 如果使用手机号找回密码
            elif data.get('type') == 'phone':
                # 先寻找该手机号是否注册
                if not CustomUser.objects.filter(phone=target).exists():
                    return JsonResponse({'message': '该手机号未注册', 'error': 1})
                # 再生成验证码
                cache_key = f'forgot_verification_code_{target}'
                cache.set(cache_key, verification_code, timeout=300)  # Set a timeout, e.g., 5 minutes
                print(f"向 {target} 这个手机号码发送了验证码: {verification_code}")

            else:
                return JsonResponse({'message': '缺少参数', 'error': 1})
            return JsonResponse({'message': '验证码发送成功', 'error': 0})
        else:
            return JsonResponse({'message': '缺少参数', 'error': 1})
    except Exception as e:
        return JsonResponse({'message': '内部错误' + str(e), 'error': 1})


def forgot_password_view(request):
# 忘记密码
    return JsonResponse({'message': '非法请求'}, status=400)

def is_token_valid_view(request):
    # 判断token是否有效
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        token = data.get('token')
        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return JsonResponse({'message': 'token无效', 'error': 1})
        else:
            return JsonResponse({'message': 'token有效', 'error': 0})
    return JsonResponse({'message': '非法请求'}, status=400)
