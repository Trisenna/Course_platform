"""
URL configuration for MyWork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework import routers, permissions
from rest_framework.documentation import include_docs_urls

from MyWork.views import Login

router = routers.DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="测试工程API",
        default_version='v1.0',
        description="测试工程接口文档",

        contact=openapi.Contact(email="22301022@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
  # YOUR PATTERNS

    path('admin/', admin.site.urls),
    # 学生
    path('student/', include('student.urls')),
    # 教师
    path('teacher/', include('teacher.urls')),
    # 管理员
    path('admins/', include('admins.urls')),
    # 配置drf-yasg路由
    # 其他 URL 模式...
# 配置django-rest-framwork API路由
    # 配置django-rest-framwork API路由

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('docs/', include_docs_urls(title='测试工程API')),
    #生成接口文档json格式
    path('swagger-json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    #登录url
    path('login/', Login.as_view(), name='login'),




    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

