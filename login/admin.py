from django.contrib import admin
from login.models import Student, Teacher
# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'grade', 'gender', 'faculty', 'email')
    list_filter = ('grade', 'faculty', 'gender')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'gender', 'faculty', 'email')
    list_filter = ('faculty', 'gender')


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)