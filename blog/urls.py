"""blog URL Configuration

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
    1. Import the include() function: from django.urls.py import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls.py'))
"""
from django.contrib import admin
from django.urls import path, include

# from django.http import HttpResponse

# # 1.导入系统的logging
# import logging
#
# # 2.创建（获取）日志器
# logger = logging.getLogger('django')
#
#
# # 3.使用日志器记录信息
# def log(request):
#     logger.info('info')
#     return HttpResponse("test")


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', log),
    # include 参数为一个元祖，两个参数
    # urlconf：子应用的路由
    # app_name：子应用的名字
    path('', include(('users.urls', 'users'), namespace='users')),
    path('', include(('home.urls', 'home'), namespace='home')),
]

# 图片访问的路由
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
