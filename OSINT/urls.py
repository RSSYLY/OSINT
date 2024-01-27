"""OSINT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

import OSINT_DB.views
import OSINT_django.views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/get_all_objects', OSINT_DB.views.get_all_objects),
    path('api/get_all_events', OSINT_DB.views.get_all_events),
    path('api/add_event', OSINT_DB.views.add_event),
    path('api/update_event/<int:event_id>', OSINT_DB.views.update_event),
    path('api/delete_event/<int:event_id>', OSINT_DB.views.delete_event),
    path('api/add_object', OSINT_DB.views.add_object),
    path('api/update_object/<int:object_id>', OSINT_DB.views.update_object),
    path('api/delete_object/<int:object_id>', OSINT_DB.views.delete_object),
    path('api/get_all_keywords', OSINT_DB.views.get_all_keywords),
    path('api/add_keyword', OSINT_DB.views.add_keyword),
    path('api/update_keyword/<int:keyword_id>', OSINT_DB.views.update_keyword),
    path('api/delete_keyword/<int:keyword_id>', OSINT_DB.views.delete_keyword),
    path('api/check_event', OSINT_DB.views.check_event),

    # ——————————django相关的api————————————————
    path('api/login/', OSINT_django.views.login),
    path('api/register/', OSINT_django.views.register),
    path('api/register/sendcode/', OSINT_django.views.register_sendcode),
    path('api/find-password/sendcode/', OSINT_django.views.find_password_sendcode),
    path('api/find-password/', OSINT_django.views.find_password),
    path('api/change-password/', OSINT_django.views.change_password),
    path('api/change_permission/', OSINT_django.views.change_permission),
    # path('logout/', views.logout),
    # path('index/', views.index),
    # path('api/get_all_users', OSINT_django.views.get_all_users),
    # path('api/home/', views.home),

    # ——————————用户管理相关的api——————————————
    path('api/user_stats/', OSINT_django.views.user_stats),
    path('api/get_all_users_info/', OSINT_django.views.get_all_users_info),

]
