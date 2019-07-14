from django.shortcuts import render

from PythonDjango.settings import BASE_DIR
from plan.models import Plan, Rubric
from scripts.import_from_excel import imp_1, imp_2, imp_3, imp_4

global s

def index(request):
    return render(request, 'plan/index.html')


def kostil(s):
    c = s.rfind('/')
    s = s[:c]
    c = s.rfind('/')
    return s[:c + 1] + 'post/', s[:c + 1] + 'postr/'

#
def view(request):
    s = ""
    plans = Plan.objects.all()
    rubrics = Rubric.objects.all()
    # Костильчик
    dir, dir2 = kostil(request.build_absolute_uri())
    # кінець костильчика
    context = {'plans': plans, 'rubrics': rubrics, 'dir': dir, 'dir2': dir2}
    return render(request, 'plan/index.html', context)



def post(request, id):
    plans = Plan.objects.filter(id=id)
    context = {'plans': plans}
    return render(request, 'plan/post.html', context)

def getjson(request):
    context = {'s': s}
    return render(request, 'plan/index.html', context)

def postr(request, r_id):
    plans = Plan.objects.filter(r_id=r_id)
    index_plans = []
    dir, dir2 = kostil(request.build_absolute_uri())
    s = ""
    for plan in plans:
        index_plans.append(dir2+str(plan.id))
        s += dir2+str(plan.id)+','
    s = s[:-1]
    # index_plans = {}
    # for counter, plan in enumerate(plans):
    #     index_plans[counter+1] = plan
    context = {'plans': plans, 'index_plans': index_plans, 's': s, 'dir': dir, 'dir2': dir2}
    return render(request, 'plan/post.html', context)


def imp_from_excel(request):
    # imp_1(None)
    return render(request, 'plan/index.html')
