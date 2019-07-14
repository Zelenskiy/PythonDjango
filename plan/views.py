

from django.shortcuts import render

from PythonDjango.settings import BASE_DIR
from plan.models import Plan, Rubric
from scripts.import_from_excel import imp_1, imp_2, imp_3, imp_4


def index(request):
    return render(request, 'plan/index.html')


def view(request, id):
    plans = Plan.objects.filter(id=id)
    # plans = Plan.objects.filter(r_id=r_id)
    # plans = Plan.objects.filter(r_id__name='Контрольно-аналітична діяльність')
    # plans = Plan.objects.filter(r_id = 29)
    # plans = Plan.objects.all()
    rubrics = Rubric.objects.all()
    s = request.build_absolute_uri()
    c = s.rfind('/')
    s = s[:c]
    c = s.rfind('/')
    dir = s[:c + 1] + 'post/'
    context = {'plans': plans, 'rubrics': rubrics, 'dir': dir}
    return render(request, 'plan/index.html', context)


def post(request, id):
    plans = Plan.objects.filter(id=id)
    context = {'plans': plans }
    return render(request, 'plan/post.html', context)


def imp_from_excel(request):
    # imp_1(None)
    return render(request, 'plan/index.html')
