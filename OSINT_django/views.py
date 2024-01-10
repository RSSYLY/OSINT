import hashlib
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect, HttpResponse

from OSINT_django.models import *


def index(request):
    pass
    return render(request, 'login/index.html')


@api_view(['POST', ])
def login(request):
    if request.method == 'POST':
        user = request.data['msg']
        name = user['name']
        pwd = user['pwd']
        admin = User.objects.filter(s_username=name, i_groupid=1)
        if len(admin) == 0:
            return HttpResponse('not have this user !!!')
        else:
            # md5加密，不用管
            h1 = hashlib.md5()
            h1.update(pwd.encode(encoding='utf-8'))
            if admin[0].s_pwd == h1.hexdigest():
                # 设置session中的值，注意要先新建django-session这个表 ！！
                request.session['user_id'] = admin[0].s_username
                return HttpResponse('login success!')
            else:
                return HttpResponse('password error!')


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
