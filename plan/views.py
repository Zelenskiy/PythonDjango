from django.shortcuts import render

from PythonDjango.settings import BASE_DIR
from plan.forms import PlanForm
from plan.models import Plan, Rubric, Responsibl
from scripts.import_from_excel import imp_1, imp_2, imp_3, imp_4
from django.utils.html import escape

global s

def index(request):
    return render(request, 'plan/index.html')


def kostil(s):
    c = s.rfind('/')
    s = s[:c]
    c = s.rfind('/')
    return s[:c + 1] + 'post/', s[:c + 1] + 'postr/'

def make_rubrics(rubrics):
    rubrics_code = ''
    for rubric in rubrics:
        rubrics_code += ' <option id="'+ str(rubric.id) +'" level="'+str(rubric.riven)+'" >'+rubric.name+'</option >'+''
    return escape(rubrics_code)

def view(request):
    s = ""
    plans = Plan.objects.all()
    rubrics = Rubric.objects.all()
    # rubrics_code = make_rubrics(rubrics)
    # Костильчик
    dir, dir2 = kostil(request.build_absolute_uri())
    # кінець костильчика
    context = {'plans': plans, 'rubrics': rubrics, 'dir': dir, 'dir2': dir2}
    return render(request, 'plan/index.html', context)



def post(request, id):
    plans = Plan.objects.filter(id=id)
    context = {'plans': plans}
    return render(request, 'plan/post.html', context)

# def getjson(request):
#     context = {'s': s}
#     return render(request, 'plan/index.html', context)

def postr(request, r_id, num):
    plans = Plan.objects.filter(r_id=r_id)
    resps = Responsibl.objects.all()
    count = len(plans)
    if count == 0:
        return render(request, 'plan/post_empty.html')
    if num >= count:
        num = count
    plan = plans[num-1]
    # form = PlanForm(instance=plans)
    context = {'plan': plan, 'num': num, 'resps': resps, 'count': count}
    return render(request, 'plan/post.html', context)


def imp_from_excel(request):
    # imp_1(None)
    return render(request, 'plan/index.html')
