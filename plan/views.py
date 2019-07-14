from django.shortcuts import render

from PythonDjango.settings import BASE_DIR
from plan.models import Plan, Rubric
from scripts.import_from_excel import imp_1, imp_2, imp_3, imp_4


def index(request):
    return render(request, 'plan/index.html')


def kostil(s):
    c = s.rfind('/')
    s = s[:c]
    c = s.rfind('/')
    return s[:c + 1] + 'post/'


def view(request, id):
    plans = Plan.objects.filter(id=id)
    # plans = Plan.objects.filter(r_id=r_id)
    # plans = Plan.objects.filter(r_id__name='Контрольно-аналітична діяльність')
    # plans = Plan.objects.filter(r_id = 29)
    # plans = Plan.objects.all()
    rubrics = Rubric.objects.all()
    # Костильчик
    dir = kostil(request.build_absolute_uri())
    # кінець костильчика
    context = {'plans': plans, 'rubrics': rubrics, 'dir': dir}
    return render(request, 'plan/index.html', context)


def post(request, id):
    plans = Plan.objects.filter(id=id)
    plan2 = plans.filter()
    context = {'plans': plans}
    return render(request, 'plan/post.html', context)


def postr(request, r_id):
    plans = Plan.objects.filter(r_id=r_id)
    # plan2 = plans.filter()
    rubrics = Rubric.objects.all()
    dir = kostil(request.build_absolute_uri())
    context = {'plans': plans, 'rubrics': rubrics, 'dir': dir}
    return render(request, 'plan/index.html', context)


def imp_from_excel(request):
    # imp_1(None)
    return render(request, 'plan/index.html')
