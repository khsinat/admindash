"""
URL configuration for adminto project.

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
from django.urls import path , include
from adminto.view import index_view, login_view,logout_view,users_view,user_detail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", view=index_view, name="index"),

path("login/", login_view, name="admin_login"),  # Login Page
    path("logout/", logout_view, name="admin_logout"),  # Logout Page
    path("users/",users_view,name="users"),
    path('user/details/<int:user_id>/', user_detail, name='user_detail'),
    #Apps
    path("apps/", include("apps.urls")),

    #Custom
    path("custom/", include("custom.urls")),

    #Components
    path("components/", include("components.urls")),
    
    # Layouts
    path("layouts/", include("layouts.urls")),

    #api 
    path('', include('api.urls')),

]
