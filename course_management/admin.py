from django.contrib import admin
from course_management.models import Course, CourseRegistration, Prerequisite, StuScore

# Register your models here.
admin.site.register([Course, CourseRegistration, StuScore])