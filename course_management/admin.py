from django.contrib import admin
from course_management.models import Course, CourseRegistration, StuScore, CourseFiles


# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_id', 'faculty', 'lecturer')
    list_filter = ('faculty', 'lecturer')


class CourseFilesAdmin(admin.ModelAdmin):
    list_display = ('course', 'file', 'add_date')
    list_filter = ('course',)


class StuScoreAdmin(admin.ModelAdmin):
    list_display = ('stu', 'course', 'score')
    list_filter = ('stu', 'course')


class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ('stu', 'course', 'is_joined')
    list_filter = ('stu', 'course', 'is_joined')


admin.site.register(CourseRegistration, CourseRegistrationAdmin)
admin.site.register(StuScore, StuScoreAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseFiles, CourseFilesAdmin)

admin.site.site_title = "学生选课系统后台管理"
admin.site.site_header = "学生选课系统后台"
