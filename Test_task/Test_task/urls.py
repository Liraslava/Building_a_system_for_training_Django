"""
URL configuration for Test_task project.

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
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import LessonListView, LessonViewListView
from .views import ProductStatisticsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lesson-views/', LessonViewListView.as_view(), name='lesson-view-list'),
    path('api/user/<int:user_id>/product/<int:product_id>/lessons/', LessonListView.as_view(), name='lesson-list'),
    path('api/product_statistics/', ProductStatisticsView.as_view(), name='product-statistics'),
]


