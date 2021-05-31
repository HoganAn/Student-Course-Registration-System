"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views
from login import views as loginViews
from course_management import views as cmViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.temp),
    path('index/', views.index, name="index"),
    path('hello/', views.hello),
    path('login/', loginViews.login_view, name="login"),
    path('signout/', loginViews.logout_view, name="logout"),
    path('signup/', loginViews.reg_view, name="signup"),
    path('personnel_info/', views.personnel_info, name="personnel_info"),
    path('course_select/', cmViews.cs_view, name="course_select"),
    path('course_selected/', cmViews.course_selected, name="course_selected"),
    path('my_course/', cmViews.my_course_view, name="my_course"),

    # Data interface
    path('get_selectable_courses/', cmViews.get_selectable_courses, name="get_selectable_courses"),
    path('get_select_stat/', cmViews.get_select_stat, name="get_select_stat"),
    path('get_my_course_list/', cmViews.get_my_course_list, name="get_my_course_list"),
]
