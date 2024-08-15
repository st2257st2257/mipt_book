"""authorization URL Configuration

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
from django.urls import path, include
from main import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'roles', views.RoleViewSet)
router.register(r'institute_group', views.InstituteGroupViewSet)
router.register(r'access', views.AccessViewSet)
router.register(r'preferences', views.PreferencesViewSet)


urlpatterns = [
    path('register/', views.register_user),
    path('admin/', admin.site.urls),
    path('base-info/', include(router.urls)),
    path('get-info/', views.IndexAuth.as_view()),
    path('token/', obtain_auth_token),
    path('test/', include('test.urls', namespace='test')),
]

