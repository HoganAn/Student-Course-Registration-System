import hashlib
from django.shortcuts import render
from django.http import HttpResponseRedirect
from login.models import Student, Teacher


# Create your views here.
def login_view(request):
    if request.method == 'GET':
        if request.session.get('is_login'):
            return HttpResponseRedirect('/index/')
        return render(request, "login.html")

    elif request.method == 'POST':
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        usr_type = request.POST.get('usr_type')
        md5 = hashlib.md5()
        md5.update(password.encode())
        password_m = md5.hexdigest()

        # if not uid:
        #     error = '请输入学号/教工号!'
        #     return render(request, 'login.html', {'error': error})
        # if not password:
        #     error = '请输入密码！'
        #     return render(request, 'login.html', {'error': error})

        if usr_type == 'student':
            usr = Student.objects.filter(uid=uid, password=password_m)
            if not usr:
                error = '用户不存在或密码错误!'
                return render(request, 'login.html', {'error': error})
            else:
                usr = usr[0]
                request.session['is_login'] = True
                request.session['uid'] = uid
                request.session['name'] = usr.name
                request.session['usr_type'] = usr_type
                response = HttpResponseRedirect('/index/')
        else:
            usr = Teacher.objects.filter(uid=uid, password=password_m)
            if not usr:
                error = '用户不存在或密码错误!'
                return render(request, 'login.html', {'error': error})
            else:
                usr = usr[0]
                request.session['is_login'] = True
                request.session['uid'] = uid
                request.session['name'] = usr.name
                request.session['usr_type'] = usr_type
                response = HttpResponseRedirect('/index/')

        return response


def reg_view(request):
    if request.method == 'GET':
        if request.session.get('is_login'):
            return HttpResponseRedirect('/index')
        return render(request, "register.html")
    elif request.method == 'POST':
        usr_type = request.POST.get('usr_type')
        uid = request.POST.get('uid')
        password = request.POST.get('password')
        md5 = hashlib.md5()
        md5.update(password.encode())
        password_md5 = md5.hexdigest()

        try:
            if usr_type == 'student':
                Student.objects.get(id=uid)
            else:
                Teacher.objects.get(id=uid)
            error = '用户已被注册！'
            return render(request, 'register.html', locals())

        except Exception as e:
            reg_form = request.POST
            if usr_type == 'student':
                Student.objects.create(
                    uid=reg_form['uid'],
                    name=reg_form['name'],
                    gender=reg_form['gender'],
                    faculty=reg_form['faculty'],
                    email=reg_form['email'],
                    password=password_md5,
                    info=reg_form['info'],
                    grade=reg_form['grade']
                )
            else:
                Teacher.objects.create(
                    uid=reg_form['uid'],
                    name=reg_form['name'],
                    gender=reg_form['gender'],
                    faculty=reg_form['faculty'],
                    email=reg_form['email'],
                    password=password_md5,
                    info=reg_form['info']
                )
            return HttpResponseRedirect('/login/')


def logout_view(request):
    request.session.flush()
    return HttpResponseRedirect('/login/')
