from random import sample
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import base64

from django.contrib import admin
from django.http import FileResponse
from course_management.models import Course, CourseRegistration, StuScore, CourseFiles

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


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
    actions = ['select_draw', 'export']

    def select_draw(self, request, queryset):
        course_dict = {}
        for q in queryset:
            if q.is_joined == '1':
                continue
            else:
                course_dict[q.course.course_id] = []
        for q in queryset:
            if q.is_joined == '1':
                continue
            else:
                course_dict[q.course.course_id].append(q.stu)
        for c in course_dict:
            joined = CourseRegistration.objects.filter(course__course_id=c, is_joined='1').count()
            capacity = Course.objects.get(course_id=c).capacity - joined
            if capacity <= 0:
                continue
            elif capacity < len(course_dict[c]):
                draw_res = sample(course_dict[c], capacity)
                for stu in draw_res:
                    reg_stat = CourseRegistration.objects.get(stu__uid=stu.uid, course__course_id=c)
                    reg_stat.is_joined = '1'
                    reg_stat.save()
            else:
                for stu in course_dict[c]:
                    reg_stat = CourseRegistration.objects.get(stu__uid=stu.uid, course__course_id=c)
                    reg_stat.is_joined = '1'
                    reg_stat.save()
        return True

    def export(self, request, queryset):
        course_dict = {}
        course_list = []
        count_list = []
        for q in queryset:
            course_dict[q.course.course_id] = []
        for q in queryset:
            course_dict[q.course.course_id].append(q.stu)
        for course in course_dict:
            course_list.append(course)
            count_list.append(len(course_dict[course]))

        fig = plt.figure()
        plt.bar(course_list, count_list)
        plt.title('选课人数统计')

        # figfile = BytesIO()
        fig.savefig('1.png')
        f = open('1.png', 'rb')
        response = FileResponse(f)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="select_static.png"'
        return response

    select_draw.short_description = '选课抽签'
    select_draw.confirm = "确定开始抽签吗？"
    select_draw.type = 'warning'

    export.short_description = '导出柱状图'


admin.site.register(CourseRegistration, CourseRegistrationAdmin)
admin.site.register(StuScore, StuScoreAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseFiles, CourseFilesAdmin)

admin.site.site_title = "学生选课系统后台管理"
admin.site.site_header = "学生选课系统后台"
