from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
def cs_view(request):
    if request.method == 'GET':
        if not request.session.get('is_login'):
            return HttpResponseRedirect('/index/')

        uid = request.session.get('uid')
        usr_type = request.session.get('usr_type')
        usr_name = request.session.get('name')
        return render(request, "course_select.html", locals())
