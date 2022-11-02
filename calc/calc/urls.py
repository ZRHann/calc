"""calc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.empty),
    path('index/', views.index),
    path('yyec_equations/', views.yyec_equations),
    path('function/', views.function),
    path('matrix/', views.matrix),
    path('function/ajax/', views.function_ajax),
    path('BingPic/', views.BingPic),

    path('login/', views.login),
    path('login/ajax/', views.login_ajax),


    path('register/', views.register),
    path('register/ajax/', views.register_ajax),

    path('logout/ajax/', views.logout_ajax),

    path('changePassword/', views.changePassword),
    path('changePassword/ajax/', views.changePassword_ajax),

    path('AddArticle/', views.AddArticle),
    path('AddArticle/ajax/', views.AddArticle_ajax),

    path('MyArticle/', views.MyArticle),

    path('MyArticle/DeleteArticle/ajax/', views.DeleteArticle_ajax),

    path('ViewArticle/', views.ViewArticle),

    path('games/test1/', views.games_test1),
    path('games/', views.games),
    path('games/jingChess/', views.games_jingChess),
    path('games/csgov01/', views.games_csgov01),
]
