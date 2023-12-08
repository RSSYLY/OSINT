from django.urls import path
from . import views

urlpatterns = [
    path('authenticate/login/', views.login_view, name='login'),
    path('authenticate/register/', views.register_view, name='register'),
    path('authenticate/forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('authenticate/is-token-valid/', views.is_token_valid_view, name='is_token_valid'),
    # 添加其他身份验证相关路径
]