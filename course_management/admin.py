from django.contrib import admin
from course_management.models import Course, CourseRegistration, StuScore, CourseFiles

# Register your models here.
admin.site.register([Course, CourseRegistration, StuScore])
admin.site.register(CourseFiles)
