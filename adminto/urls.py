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
from adminto.view import index_view, login_view,logout_view,users_view,user_detail,page_detail,delete_user,contactus_view,total_grow_logs_view,total_analysis_view,packages_view,emails_in_queue_view,transactions_view,cms_view,notifications_view,settings_view,myprofile_view,add_page_view,view_page_view,edit_user_view,edit_page_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", view=index_view, name="index"),

    path("login/", login_view, name="admin_login"),  # Login Page
    path("logout/", logout_view, name="admin_logout"),  # Logout Page
    path("users/",users_view,name="users"),
    path("total-grow-logs/",total_grow_logs_view,name="total-grow-logs"),
    path("total-analysis/",total_analysis_view,name="total-analysis"),
    path("packages/",packages_view,name="packages"),
    path("emails-in-queue/",emails_in_queue_view,name="emails-in-queue"),
    path("transactions/",transactions_view,name="transactions"),
    path("contactus/",contactus_view,name="contactus"),
    path("cms/",cms_view,name="cms"),
    path("cms/add-page",add_page_view,name="add-page"),
    path('cms/page/<int:type_id>/', view_page_view, name='view-page'),
    path('cms/edit/<int:type_id>/', edit_page_view, name='edit-page'),
    path("notifications/",notifications_view,name="notifications"),
    path("settings/",settings_view,name="settings"),
    path("myprofile/",myprofile_view,name="myprofile"),
    path("myprofile/edit/<int:user_id>",edit_user_view,name="edit-user"),

    path('user/details/<int:user_id>/', user_detail, name='user_detail'),
    #Apps
    path("apps/", include("apps.urls")),

    #Custom
    path("custom/", include("custom.urls")),

    
    # Layouts
    path("layouts/", include("layouts.urls")),

    #api 
    path('', include('api.urls')),
    path('page/<str:type>/', page_detail, name='page_detail'),
    path('user/delete/<int:user_id>/', delete_user, name='delete_user'),

]
