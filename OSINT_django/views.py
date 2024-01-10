from django.shortcuts import HttpResponse

# from OSINT_django.models import User

"""
def index(request):
    pass
    return render(request, 'login/index.html')


@api_view(['POST', ])  # 修饰器，表示这个函数只能接受post请求，下面这一坨都是网上抄的
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # user = request.data['msg'] # 获取post请求中的参数,我不知道这是干嘛的，九敏
        name = data.get('name')
        pwd = data.get('pwd')
        admin = User.objects.filter(username=name)
        if len(admin) == 0:
            return HttpResponse('not have this user !!!')
        else:
            # md5加密
            h1 = hashlib.md5()
            h1.update(pwd.encode(encoding='utf-8'))
            if admin[0].s_pwd == h1.hexdigest():
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
"""

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if username and password and email:
            user = User.objects.create_user(username, email, password)
            user.save()
            return HttpResponse('User created successfully')
        else:
            return HttpResponse('Missing username, password or email')


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
