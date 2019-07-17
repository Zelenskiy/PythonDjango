from django.db.models import Max
from django.shortcuts import render

from PythonDjango.settings import BASE_DIR
from plan.forms import PlanForm
from plan.models import Plan, Rubric, Responsibl
from scripts.import_from_excel import imp_1, imp_2, imp_3, imp_4
from django.utils.html import escape

global s


def main(request):
    return render(request, 'plan/main.html')

