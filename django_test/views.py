from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from login.models import Student, Teacher


def hello(request):
    return HttpResponse("Hello world!")


def index(request):
    if not request.session.get('is_login'):
        return HttpResponseRedirect('/login/')
    args = {
        'usr_name': request.session.get('name'),
        'usr_type': request.session.get('usr_type'),
        'welcome': "你好！" + request.session.get('name')
    }
    return render(request, 'index.html', args)


def temp(request):
    return HttpResponseRedirect('/index/')


def personnel_info(request):
    if not request.session.get('is_login'):
        return HttpResponseRedirect('/login/')

    args = {}
    if request.session.get('usr_type') == 'student':
        usr = Student.objects.get(uid=request.session.get('uid'))
        args['grade'] = usr.grade
    else:
        usr = Teacher.objects.get(uid=request.session.get('uid'))

    args['usr_name'] = usr.name
    args['uid'] = usr.uid
    args['usr_type'] = request.session.get('usr_type')
    args['email'] = usr.email
    args['faculty'] = usr.faculty
    args['info'] = usr.info
    if usr.gender == 'male':
        args['gender'] = '男'
    else:
        args['gender'] = '女'
    return render(request, 'personnel_info.html', args)
