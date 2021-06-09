from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, FileResponse
from django.utils.http import urlquote
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings
from course_management.models import Course, CourseRegistration, CourseFiles, StuScore, Prerequisite
from login.models import Student
import os


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
            stu_count = Student.objects.filter(courseregistration__is_joined='1', course__course_id=c.course_id).count()
            if stu_count >= c.capacity:
                continue
            data = {
                'cid': c.course_id,
                'cname': c.course_name,
                'fname': c.faculty,
                'tname': c.lecturer.name,
                'capacity': c.capacity - stu_count,
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


def course_index_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    course = Course.objects.get(course_id=course_id)
    cname = course.course_name
    notice = course.notice
    intro = course.info
    cid = course_id
    return render(request, "course_index.html", locals())


def course_intro_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    course = Course.objects.get(course_id=course_id)
    cname = course.course_name
    cid = course_id
    course_intro = course.info
    return render(request, "course_intro.html", locals())


def course_files_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    course = Course.objects.get(course_id=course_id)
    cname = course.course_name
    cid = course_id
    return render(request, "s_course_files.html", locals())


def my_score_view(request):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    return render(request, "my_score.html", locals())


def t_course_manage_view(request):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    return render(request, "t_my_course.html", locals())


def t_course_index_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    course = Course.objects.get(course_id=course_id)
    cname = course.course_name
    return render(request, "t_course_index.html", locals())


def t_course_notice_view(request, course_id):
    if not request.session.get('is_login'):
        return HttpResponseRedirect('/index/')
    if request.method == 'GET':
        uid = request.session.get('uid')
        usr_type = request.session.get('usr_type')
        usr_name = request.session.get('name')
        course = Course.objects.get(course_id=course_id)
        cname = course.course_name
        notice = course.notice
        return render(request, "t_course_notice.html", locals())
    elif request.method == 'POST':
        uid = request.session.get('uid')
        usr_type = request.session.get('usr_type')
        usr_name = request.session.get('name')
        course = Course.objects.get(course_id=course_id)
        cname = course.course_name
        new_notice = request.POST.get('new_notice')
        course.notice = new_notice
        course.save()
        notice = course.notice
        return HttpResponseRedirect(reverse('t_course_notice', args=[course_id]))


def t_course_file_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
    uid = request.session.get('uid')
    usr_type = request.session.get('usr_type')
    usr_name = request.session.get('name')
    course = Course.objects.get(course_id=course_id)
    cname = course.course_name
    return render(request, "t_course_file_manage.html", locals())


def t_course_stu_manage(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
        uid = request.session.get('uid')
        usr_type = request.session.get('usr_type')
        usr_name = request.session.get('name')
        course = Course.objects.get(course_id=course_id)
        cname = course.course_name
        return render(request, "t_course_student_manage.html", locals())
    else:
        return HttpResponse(status=403)


def t_set_pre_view(request, course_id):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
        uid = request.session.get('uid')
        usr_type = request.session.get('usr_type')
        usr_name = request.session.get('name')
        course = Course.objects.get(course_id=course_id)
        cname = course.course_name
        return render(request, "t_set_pre.html", locals())
    else:
        return HttpResponse(status=403)


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


def get_my_score(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        courses = Course.objects.filter(reg_stat__uid=uid, courseregistration__is_joined='1')
        score_list = []
        for c in courses:
            data = {
                'cid': c.course_id,
                'cname': c.course_name,
                'fname': c.faculty,
                'tname': c.lecturer.name
            }
            score = StuScore.objects.filter(stu__uid=uid, course__course_id=c.course_id)
            if len(score) != 0:
                data['score'] = score[0].score
            else:
                data['score'] = '暂无成绩'
            score_list.append(data)
        data = {
            'code': 0,
            'data': score_list
        }
        return JsonResponse(data)


def get_t_my_course_list(request):
    if request.method == 'GET':
        uid = request.session.get('uid')
        courses = Course.objects.filter(lecturer__uid=uid)
        total = courses.count()
        course_info = []
        for c in courses:
            data = {
                'cid': c.course_id,
                'cname': c.course_name,
                'fname': c.faculty,
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


def get_course_file_list(request):
    if request.method == 'GET':
        cid = request.GET.get('cid')
        files = CourseFiles.objects.filter(course__course_id=cid)
        file_list = []
        for file in files:
            data = {
                "fname": file.file.name.split('/')[-1],
                "uptime": file.add_date.strftime("%Y年%m月%d日 %H:%M:%S")
            }
            file_list.append(data)
        data = {
            "code": 0,
            "data": file_list
        }
        return JsonResponse(data)


def get_stu_list(request):
    if request.method == 'GET':
        cid = request.GET.get('cid')
        students = Student.objects.filter(courseregistration__course__course_id=cid, courseregistration__is_joined='1')
        stu_list = []
        for stu in students:
            data = {
                "sid": stu.uid,
                "name": stu.name,
            }
            s = StuScore.objects.filter(course__course_id=cid, stu__uid=stu.uid)
            if len(s) != 0:
                data['score'] = s[0].score
            else:
                data['score'] = '暂无成绩'
            stu_list.append(data)
        data = {
            "code": 0,
            "data": stu_list
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)


def upload(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        cid = request.POST.get('cid')
        course = Course.objects.get(course_id=cid)
        CourseFiles.objects.create(course=course, file=file)
        data = {
            "code": 0
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)


def download(request):
    if request.method == 'GET':
        cid = request.GET.get('cid')
        fname = request.GET.get('fname')
        file_path = os.path.join(settings.MEDIA_ROOT, 'course_files', cid, fname)
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename={0}'.format(urlquote(fname))
        return response
    else:
        return HttpResponse(status=403)


def edit_score(request):
    if request.method == 'POST':
        sid = request.POST.get('sid')
        cid = request.POST.get('cid')
        score = request.POST.get('score')
        if int(score) > 100 or int(score) < 0:
            return HttpResponse('RangeErr')
        stu_score = StuScore.objects.filter(course__course_id=cid, stu__uid=sid)
        if len(stu_score) != 0:
            stu_score[0].score = score
            stu_score[0].save()
        else:
            stu = Student.objects.get(uid=sid)
            course = Course.objects.get(course_id=cid)
            StuScore.objects.create(score=score, stu=stu, course=course)
        return HttpResponse('Success')
    else:
        return HttpResponse(status=403)


def t_get_unpre(request):
    if request.method == 'GET':
        cid = request.GET.get('cid')
        pre = Prerequisite.objects.filter(course__course_id=cid)
        pre_list = []
        for c in pre:
            pre_list.append(c.pre_course_id)
        unpre_course = Course.objects.exclude(course_id__in=pre_list)
        print(unpre_course)
        course_list = []
        for c in unpre_course:
            if c.course_id == cid:
                continue
            data = {
                'cid': c.course_id,
                'name': c.course_name,
                'faculty': c.faculty,
            }
            course_list.append(data)
        data = {
            'code': 0,
            'data': course_list
        }
        return JsonResponse(data)
    else:
        return HttpResponse(status=403)


def t_set_pre(request):
    if request.method == 'POST':
        pre_cid = request.POST.get('pre_cid')
        cid = request.POST.get('cid')
        course = Course.objects.get(course_id=cid)
        pre_course = Prerequisite.objects.get_or_create(pre_course_id=pre_cid)
        course.prerequisite.add(pre_course[0])
        return HttpResponse('Success')
    else:
        return HttpResponse(status=403)
