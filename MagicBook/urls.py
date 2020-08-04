"""MagicBook URL Configuration

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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from article.views import article_list
import notifications.urls
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # 新增代码，article的路由
    path('', article_list, name='home'),
    path('', include('article.urls', namespace='article')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    # 用户管理
    path('userprofile/', include('userprofile.urls', namespace='userprofile')),
    #密码验证路由
    # path('password-reset/', include('password_reset.urls')),
    # 评论
    path('comment/', include('comment.urls', namespace='comment')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # notice
    path('notice/', include('notice.urls', namespace='notice')),
    # path('search/', views.search, name="search"),

 ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
