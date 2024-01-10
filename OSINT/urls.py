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
from django.contrib import admin
from django.urls import path
import OSINT_DB.views
from OSINT_django import views
urlpatterns = [
    path('admin/', admin.site.urls),
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
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),

]