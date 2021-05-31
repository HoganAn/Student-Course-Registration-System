from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.core import serializers
from course_management.models import Course, CourseRegistration, Prerequisite
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
        return JsonResponse(data)
    else:
        return HttpResponse(status=405)


def get_select_stat(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        courses = Course.objects.filter(reg_stat__uid=uid)
        course_list = []
        for c in courses:
            stat = CourseRegistration.objects.get(course__course_id=c.course_id).is_joined
            data = {
                'cid': c.course_id,
                'cname': c.course_name,
                'fname': c.faculty,
                'tname': c.lecturer.name,
                'cstat': stat
            }
            course_list.append(data)
        data = {
            'code': 0,
            'data': course_list
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=405)


def course_selected(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        uid = request.session.get('uid')
        course = Course.objects.get(course_id=cid)
        stu = Student.objects.get(uid=uid)
        pre_courses = course.prerequisite.all()
        for pc in pre_courses:
            stat = Course.objects.filter(course_id=pc.pre_course_id,
                                         reg_stat__uid=uid,
                                         courseregistration__is_joined='1')
            if len(stat) == 0:
                return HttpResponse('UnmetRequirement')

        course.reg_stat.add(stu, through_defaults={'is_joined': '0'})
        return HttpResponse('Success')
    else:
        return HttpResponse(status=405)


def my_course_view(request):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')

        uid = request.session.get('uid')
        usr_type = request.session.get('usr_type')
        usr_name = request.session.get('name')
        return render(request, "my_course.html", locals())


def get_my_course_list(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        courses = Course.objects.filter(reg_stat__uid=uid, courseregistration__is_joined='1')
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
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)
