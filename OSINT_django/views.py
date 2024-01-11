import hashlib
import json

from django.shortcuts import HttpResponse
from rest_framework.decorators import api_view


# from OSINT_django.models import User


@api_view(['POST', ])
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        users = User.objects.filter(username=username)
        if len(users) == 0:
            return HttpResponse('User does not exist')
        else:
            h1 = hashlib.md5()
            h1.update(password.encode(encoding='utf-8'))
            if users[0].password == h1.hexdigest():
                request.session['user_id'] = users[0].username
                return HttpResponse('Login successful')
            else:
                return HttpResponse('Password error')


"""
@api_view(['GET', ])
def home(request):
    if request.method == 'GET':
        try:
            print(request.COOKIES['sessionid'])
            print(request.session['user_id'])
        except Exception as e:
            print(e)
            return HttpResponse('login error !')
        return HttpResponse('login success !')


# 登出功能，清除session
@api_view(['GET', ])
def login_out(request):
    request.session.flush()
    return HttpResponse('login out !')


def register(request):
    pass
    return render(request, 'login/register.html')


def logout(request):
    pass
    return redirect('/index/')




"""


def register(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if username and password and email:
            # 计算密码的 MD5 哈希值
            h1 = hashlib.md5()
            h1.update(password.encode(encoding='utf-8'))
            hashed_password = h1.hexdigest()
            # 使用哈希密码创建用户
            user = User.objects.create_user(username, email, hashed_password)
            user.save()
            return HttpResponse('User created successfully')
        else:
            return HttpResponse('Missing username, password or email')


"""
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('User logged in')
            else:
                return HttpResponse('Invalid credentials')
        else:
            return HttpResponse('Missing username or password')
"""

from django.contrib.auth.models import User
from django.http import JsonResponse


def get_all_users(request):
    users = User.objects.all()
    user_list = list(users.values('username', 'email'))
    return JsonResponse(user_list, safe=False)
