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
from django.contrib import admin
from django.urls import path
from . import views
from login import views as loginViews
from course_management import views as cmViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.temp),
    path('index/', views.index, name="index"),
    path('login/', loginViews.login_view, name="login"),
    path('signout/', loginViews.logout_view, name="logout"),
    path('signup/', loginViews.reg_view, name="signup"),
    path('personnel_info/', views.personnel_info, name="personnel_info"),
    path('course_select/', cmViews.cs_view, name="course_select"),
    path('course_selected/', cmViews.course_selected, name="course_selected"),
    path('my_course/', cmViews.my_course_view, name="my_course"),
    path('my_course/score', cmViews.my_score_view, name="my_score"),
    path('my_course/<slug:course_id>', cmViews.course_index_view, name="course_info"),
    path('my_course/<slug:course_id>/intro', cmViews.course_intro_view, name="course_intro"),
    path('my_course/<slug:course_id>/course_files', cmViews.course_files_view, name="course_files"),
    path('course_manage/', cmViews.t_course_manage_view, name="t_course_manage"),
    path('course_manage/<slug:course_id>/', cmViews.t_course_index_view, name="t_course_index"),
    path('course_manage/<slug:course_id>/file_manage/', cmViews.t_course_file_view, name="t_course_file"),
    path('course_manage/<slug:course_id>/notice/', cmViews.t_course_notice_view, name="t_course_notice"),
    path('course_manage/<slug:course_id>/student_manage/', cmViews.t_course_stu_manage, name="t_stu_manage"),
    path('course_manage/<slug:course_id>/set_pre', cmViews.t_set_pre_view, name="t_set_pre"),

    # Data interface
    path('get_selectable_courses/', cmViews.get_selectable_courses, name="get_selectable_courses"),
    path('get_select_stat/', cmViews.get_select_stat, name="get_select_stat"),
    path('get_my_course_list/', cmViews.get_my_course_list, name="get_my_course_list"),
    path('get_t_my_course_list/', cmViews.get_t_my_course_list, name="get_t_my_course_list"),
    path('get_t_stu_list/', cmViews.get_stu_list, name="get_stu_list"),
    path('upload/', cmViews.upload, name="upload"),
    path('get_file_list/', cmViews.get_course_file_list, name="get_file_list"),
    path('download/', cmViews.download, name="download"),
    path('edit_score/', cmViews.edit_score, name="edit_score"),
    path('get_unpre', cmViews.t_get_unpre, name="get_unpre"),
    path('set_pre/', cmViews.t_set_pre, name="set_pre"),
    path('get_my_score/', cmViews.get_my_score, name="get_my_score")
]
