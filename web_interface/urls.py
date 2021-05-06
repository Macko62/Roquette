"""web_interface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from pages import views as pViews
from sign_messages.views import (
    api_get,
    api_put
    )

urlpatterns = [
    path('',pViews.index_view,name='Home'),
    path('index',pViews.index_view,name='Home'),
    path('index/',pViews.index_view,name='Home'),
    path('index.html',pViews.index_view,name='Home'),
    path('account/login/index.html',pViews.index_view,name='Home'),
    path('home',pViews.index_view,name='Home'),
    path('home/',pViews.index_view,name='Home'),
    path('home.html',pViews.index_view,name='Home'),
    path('settings',pViews.settings_view,name='Home'),
    path('settings/',pViews.settings_view,name='Home'),
    path('settings.html',pViews.settings_view,name='Home'),
    path('account/login/settings.html',pViews.settings_view,name='Home'),
    path('admin/', admin.site.urls),
    path('get/',api_get,name='apiget'),
    path('put/',api_put,name='apiput'),
    path('account/', include('accounts.urls')),
    path('sign/',pViews.sign,name='Sign'),
]
