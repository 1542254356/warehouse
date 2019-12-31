"""sjk URL Configuration

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
from app.views import index_login, register, infomanage, index, infochange, index_logout, outstore, instore

urlpatterns = [
    path('admin/', admin.site.urls, name= 'admin'),
    path('', index, name= 'index'),
    path('login/', index_login,name= 'login'),
    path('logout/', index_logout, name='logout'),
    path('register/', register, name= 'register'),
    path('infomanage/',infomanage, name= 'infomanage' ),
    path('infochange/', infochange, name= 'infochange'),
    path('instore/', instore, name= 'instore'),
    path('outstore/', outstore, name= 'outstore'),
]