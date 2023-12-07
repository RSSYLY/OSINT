from django.urls import path
from . import views

urlpatterns = [
    path('authenticate/login/', views.login_view, name='login'),
    path('authenticate/register/', views.register_view, name='register'),
    path('authenticate/forgot-password/', views.forgot_password_view, name='forgot_password'),
    # 添加其他身份验证相关路径
]