from django.views.generic.edit import FormView
# from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import UserCreationForm
from django.db.models import Max
from django.shortcuts import render
# from django.views.generic import FormView

from plan.forms import PlanForm, UserRegistrationForm
from plan.models import Plan, Rubric
from django.utils.html import escape



def index(request):
    return render(request, 'plan/index.html')

def login(request):
    return render(request, 'registration/login.html.html')


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

def add(request):
    if request.method == "POST":
        plan = {}
        context = {'plan': plan}
        return render(request, 'plan/post.html', context)

def view(request):
    s = ""
    plans = Plan.objects.all()
    rubrics = Rubric.objects.all()
    rubr_id_max = Rubric.objects.aggregate(Max('id'))
    # rubrics_code = make_rubrics(rubrics)
    # Костильчик
    dir, dir2 = kostil(request.build_absolute_uri())
    # кінець костильчика
    context = {'plans': plans, 'rubrics': rubrics, 'dir': dir, 'dir2': dir2, 'rubr_id_max': rubr_id_max}
    return render(request, 'plan/index.html', context)


def post(request, id):
    plans = Plan.objects.filter(id=id)
    context = {'plans': plans}
    return render(request, 'plan/post.html', context)

def postr(request, r_id, num):
    plans = Plan.objects.filter(r_id=r_id)
    if request.method == "POST":
        pass
    else:
        # resps = Responsibl.objects.all()
        count = len(plans)
        if count == 0:
            return render(request, 'plan/post_empty.html')
        if num >= count:
            num = count
        plan = plans[num - 1]
        i_id = plan.id
        form = PlanForm(instance=plan)
        context = {'num': num, 'count': count, 'form': form, 'i_id': i_id}
    return render(request, 'plan/post.html', context)


def imp_from_excel(request):
    # imp_1(None)
    return render(request, 'plan/index.html')

# Вариант регистрации на базе класса FormView
class MyRegisterFormView(FormView):
    # Указажем какую форму мы будем использовать для регистрации наших пользователей, в нашем случае
    # это UserCreationForm - стандартный класс Django унаследованный
    form_class = UserRegistrationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
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

