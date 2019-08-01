import os
from xml.dom.minidom import Document

import docx
from django.http import HttpResponse, FileResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormView
from django.db.models import Max
from docx.table import Table

from PythonDjango.settings import MEDIA_DIR
from scripts.import_from_excel import start_import
from worktime.models import Settings
from .forms import PlanForm, UserRegistrationForm
from .models import Plan, Rubric, Direction, Purpose, Plantable
from django.utils.html import escape
from .utils import *

from docxtpl import DocxTemplate


def index(request):
    return render(request, 'plan/index.html')


def ribbon(request):
    s = Settings.objects.filter(field='plantable')[0].value
    table = Plantable.objects.get(pk=int(s))
    rubrics = Rubric.objects.filter(plantable_id=table)
    rubr_id_max = Rubric.objects.aggregate(Max('id'))
    context = {'rubrics': rubrics, 'rubr_id_max': rubr_id_max}
    return render(request, 'plan/ribbon.html', context)


# def updplan (request, id):
#     data = request.POST
#     p = Plan.objects.get(pk=id)
#
#
#
#     context = {}
#     return render(request, 'plan/ribbview.html', context)

def ribbview(request, r_id):
    # form = PlanForm()
    s = Settings.objects.filter(field='plantable')[0].value
    table = Plantable.objects.get(pk=int(s))
    plans = Plan.objects.filter(plantable_id=table, r_id=r_id)
    context = {'plans': plans}
    return render(request, 'plan/ribbview.html', context)


def login(request):
    return render(request, 'registration/login.html')


def kostil(s):
    c = s.rfind('/')
    s = s[:c]
    c = s.rfind('/')
    return s[:c + 1] + 'post/', s[:c + 1] + 'postr/'


def make_rubrics(rubrics):
    rubrics_code = ''
    for rubric in rubrics:
        rubrics_code += ' <option id="' + str(rubric.id) + '" level="' + str(
            rubric.riven) + '" >' + rubric.name + '</option >' + ''
    return escape(rubrics_code)


def view(request):
    s = Settings.objects.filter(field='plantable')[0].value
    table = Plantable.objects.get(pk=int(s))
    plans = Plan.objects.filter(plantable_id=table)
    rubrics = Rubric.objects.filter(plantable_id=table)
    rubr_id_max = Rubric.objects.aggregate(Max('id'))
    dir, dir2 = kostil(request.build_absolute_uri())
    context = {'plans': plans, 'rubrics': rubrics, 'dir': dir, 'dir2': dir2, 'rubr_id_max': rubr_id_max}
    # return render(request, reverse_lazy('index'), context)
    return render(request, 'plan/index.html', context)


def post(request, id):
    s = Settings.objects.filter(field='plantable')[0].value
    table = Plantable.objects.get(pk=int(s))
    plans = Plan.objects.filter(plantable_id=table)
    context = {'plans': plans}
    return render(request, 'plan/post.html', context)


def verification_user_permission_for_write(request):
    if request.user.is_authenticated:
        if request.user.has_perm('plan.change_plan'):
            print("Можу міняти")
        if request.user.has_perm('plan.view_plan'):
            print("Можу дивитися")

        # perm = User.user_permissions.

        username = request.user
    # print(username)
    return username


class Post_delete(View):

    def post(self, request, id):
        post = Plan.objects.get(pk=id)
        post.delete()
        context = {}
        return render(request, 'plan/post.html', context)


def postr(request, r_id, num):
    verification_user_permission_for_write(request)
    s = Settings.objects.filter(field='plantable')[0].value
    table = Plantable.objects.get(pk=int(s))

    if (num > 0) and (request.user.has_perm('plan.view_plan')):
        plans = Plan.objects.filter(plantable_id=table, r_id=r_id)
        count = len(plans)
        if count == 0:
            return render(request, 'plan/post_empty.html')
        if num >= count:
            num = count
        plan = plans[num - 1]
        i_id = plan.id
        form = PlanForm(instance=plan)
        if request.method == "POST":
            form.save()
            context = {'num': num, 'count': count, 'form': form, 'r_id': r_id, 'i_id': i_id}
            return render(request, '', context)

        else:
            context = {'num': num, 'count': count, 'form': form, 'r_id': r_id, 'i_id': i_id}
            return render(request, 'plan/post.html', context)
    else:
        if request.user.has_perm('plan.add_plan'):
            plan = Plan()
            plan.r_id = Rubric.objects.get(pk=int(r_id))
            plan.content = ''
            plan.responsible = ''
            plan.termin = ''
            plan.generalization = ''
            plan.note = ''
            plan.direction_id = Direction.objects.filter(name='')[0]
            plan.purpose_id = Purpose.objects.filter(name='')[0]
            max_sort_fild = Plan.objects.filter(r_id=r_id).aggregate(Max('sort'))
            srt = max_sort_fild['sort__max']
            plan.sort = srt + 1
            plan.plantable_id = Plantable.objects.get(pk=12)
            plan.save()
            form = PlanForm(instance=plan)
            i_id = plan.id
            plans = Plan.objects.filter(r_id=r_id, plantable_id=table)
            count = len(plans)
            num = count
            context = {'num': num, 'count': count, 'form': form, 'r_id': r_id, 'i_id': i_id}
            return render(request, 'plan/post.html', context)


def imp_from_excel(request):
    start_import()
    return render(request, 'plan/import_end.html')


@csrf_exempt
def rib_del_plan(request, id):
    print("Вилучамо id=", id)
    Plan.objects.get(pk=id).delete()
    return render(request, 'plan/ribbview.html', {})


@csrf_exempt
def rib_update_plan(request, id, num_field):
    if request.POST and request.is_ajax() and request.user.has_perm('plan.change_plan'):
        data = request.POST
        p = Plan.objects.get(pk=id)
        map = {1: 'id', 2: 'direction_id', 3: 'purpose_id', 4: 'content', 5: 'termin', 6: 'generalization',
               7: 'responsible', 8: 'note'}

        if num_field == 4:
            p.content = data['content']
            p.save()
        elif num_field == 5:
            p.termin = data['termin']
            p.save()
        elif num_field == 6:
            p.generalization = data['generalization']
            p.save()
        elif num_field == 7:
            p.responsible = data['responsible']
            p.save()
        elif num_field == 8:
            p.note = data['note']
            p.save()
        elif num_field == 9:
            s = float(data['sort'].replace(",", "."))
            p.sort = s
            p.save()
        elif num_field == 10:
            p.show = not p.show
            p.save()
        elif num_field == 0:
            p.content = data['content']
            p.termin = data['termin']
            p.generalization = data['generalization']
            p.responsible = data['responsible']
            p.note = data['note']
            p.save()

        # print(map[num_field])

        # if data['direction_id'] == '':
        #     p.direction_id = Direction.objects.get(pk=0)
        # else:
        #     p.direction_id = Direction.objects.get(pk=int(data['direction_id']))
        # if data['purpose_id'] == '':
        #     p.purpose_id = Purpose.objects.get(pk=0)
        # else:
        #     p.purpose_id = Purpose.objects.get(pk=int(data['purpose_id']))
        # p.content = data['content']
        # p.generalization = data['generalization']
        # p.responsible = data['responsible']
        # p.termin = data['termin']
        # p.note = data['note']

    return render(request, 'plan/ribbview.html', {})


@csrf_exempt
def rib_add_plan(request):
    if request.POST and request.is_ajax() and request.user.has_perm('plan.change_plan'):
        data = request.POST
        p = Plan()

        p.content = data['content']
        p.termin = data['termin']
        p.generalization = data['generalization']
        p.responsible = data['responsible']
        p.sort = float(data['sort'].replace(",", "."))
        p.note = data['note']

        pltable = data['plantable']
        pt = Plantable.objects.get(pk=int(pltable))
        p.plantable_id = pt

        rtable = data['rtable']
        rt = Rubric.objects.filter(name=rtable)[0]

        p.r_id = rt
        p.save()

        # print(map[num_field])

        # if data['direction_id'] == '':
        #     p.direction_id = Direction.objects.get(pk=0)
        # else:
        #     p.direction_id = Direction.objects.get(pk=int(data['direction_id']))
        # if data['purpose_id'] == '':
        #     p.purpose_id = Purpose.objects.get(pk=0)
        # else:
        #     p.purpose_id = Purpose.objects.get(pk=int(data['purpose_id']))
        # p.content = data['content']
        # p.generalization = data['generalization']
        # p.responsible = data['responsible']
        # p.termin = data['termin']
        # p.note = data['note']

    return render(request, 'plan/ribbview.html', {})


def update_plan(request, id):
    if request.POST and request.is_ajax() and request.user.has_perm('plan.change_plan'):
        data = request.POST
        p = Plan.objects.get(pk=id)
        if data['direction_id'] == '':
            p.direction_id = Direction.objects.get(pk=0)
        else:
            p.direction_id = Direction.objects.get(pk=int(data['direction_id']))
        if data['purpose_id'] == '':
            p.purpose_id = Purpose.objects.get(pk=0)
        else:
            p.purpose_id = Purpose.objects.get(pk=int(data['purpose_id']))
        p.content = data['content']
        p.generalization = data['generalization']
        p.responsible = data['responsible']
        p.termin = data['termin']
        p.note = data['note']
        p.save()
    return render(request, 'plan/post.html', {})


class MyRegisterFormView(FormView):
    form_class = UserRegistrationForm
    success_url = "../../plan/view/"
    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        # Функция super( тип [ , объект или тип ] )
        # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)


def export_word(request):
    #     http://www.ilnurgi1.ru/docs/python/modules_user/docx.html
    #   https://python-docx.readthedocs.io/en/latest/user/quickstart.html

    doc = docx.Document()
    doc.add_paragraph('Hello world')
    table = doc.add_table(rows=2, cols=2)

    table.style = 'LightShading-Accent1'

    filename = os.path.join(MEDIA_DIR, 'report', 'plan.docx')  # r'd:/MyDoc/PythonDjango/plan.docx'

    doc.save(filename)
    # return render(request, 'plan/ribbon.html', {})
    return FileResponse(open(filename, 'rb'), as_attachment=True)
