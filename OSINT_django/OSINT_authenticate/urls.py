from django.urls import path
from . import views

urlpatterns = [
    path('authenticate/login/', views.login_view, name='login'),
    path('authenticate/register/send-code/', views.register_send_verification_code, name='register_send_verification_code'),
    path('authenticate/register/', views.register_user, name='register'),
    path('authenticate/forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('authenticate/forgot-password/send-code/', views.forgot_password_send_verification_code, name='forgot_password_send_verification_code'),
    path('authenticate/is-token-valid/', views.is_token_valid_view, name='is_token_valid'),
    # 添加其他身份验证相关路径
]