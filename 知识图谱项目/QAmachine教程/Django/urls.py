"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from QAManagement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path(r'accurate_search/', views.accurate_search),
    path(r'usermayask/', views.usermayask),
    path(r'type_search/', views.type_search),


# 实现问题在页面使用气泡展示
    path(r'gulugulu/', views.answer),
    path(r'guluanswer/', views.jsons),
]
