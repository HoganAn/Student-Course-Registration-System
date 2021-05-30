from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.core import serializers
from course_management.models import Course, CourseRegistration
from login.models import Student
import json


def cs_view(request):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')

        uid = request.session.get('uid')
        usr_type = request.session.get('usr_type')
        usr_name = request.session.get('name')
        return render(request, "course_select.html", locals())


def get_selectable_courses(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        courses = Course.objects.exclude(reg_stat__uid=uid)
        total = courses.count()
        course_info = []
        for c in courses:
            data = {
                'cid': c.course_id,
                'cname': c.course_name,
                'fname': c.faculty,
                'tname': c.lecturer.name,
                'cinfo': c.info
            }
            course_info.append(data)

        data = {
            'code': 0,
            'count': total,
            'data': course_info
        }

        return JsonResponse(data, safe=False)


def course_selected(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        uid = request.session.get('uid')
        course = Course.objects.get(course_id=cid)
        stu = Student.objects.get(uid=uid)
        course.reg_stat.add(stu, through_defaults={'is_joined': '0'})
        # CourseRegistration.objects.create(stu=uid, course=cid, is_joined=0)
        return HttpResponse('success')
        # return render(request, "course_select.html")

    else:
        return HttpResponse(status=405)
