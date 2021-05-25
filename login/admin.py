from django.contrib import admin
from login.models import Student, Teacher
# Register your models here.


admin.site.register([Student, Teacher])
