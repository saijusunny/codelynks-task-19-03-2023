from django import views
from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
   
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('signup/', views.signup, name='signup'),
    path('usercreate/', views.usercreate, name='usercreate'),
    path('home/', views.home, name='home'),
    path('user_management/', views.user_management, name='user_management'), 
    path('profile_user/', views.profile_user, name='profile_user'),
    path('logout/', views.logout, name='logout'),
    path('editpro/<int:pk>', views.editpro, name='editpro'),
    path('home_user/', views.home_user, name='home_user'),
    path('up_pro/<int:id>', views.up_pro, name='up_pro'),

    path('feeds/', views.feeds, name='feeds'),
    path('feeds_user/', views.feeds_user, name='feeds_user'),
     path('create_posts/', views.create_posts, name='create_posts'),
    path('create_post/', views.create_post, name='create_post'),
    path('add_lk/', views.add_lk, name='add_lk'),
    path('add_dlk/', views.add_dlk, name='add_dlk'),
    path('view_like/<int:id>', views.view_like, name='view_like'),
    
]