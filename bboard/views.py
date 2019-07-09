from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Bb, Rubric
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from .forms import BbForm
from django import forms


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

def post_detail(request, slug):
    post = Bb.objects.get(slug__iexact=slug)
    return render(request, 'bboard/post_detail.html', context={'post': post})


def edit(request, slug):
    post = get_object_or_404(Bb, slug__iexact=slug)
    # post = Bb.objects.get(slug__iexact=slug)
    if request.method == "POST":
        # form = BbForm(data=request.POST, instance=post)
        form = BbForm(request.POST)
        if form.is_valid():
            if 'photo' in request.FILES:
                form.photo = request.FILES['photo']
            post = form.save(commit=False)
            #К примеру меняем одно поле сами, если не нужно, то просто сохраняем
            post.moder = 0
            post.save()
            return redirect('../../')
    else:
        form = BbForm(instance=post)
    return render(request, 'bboard/edit.html', {'form': form})



# def add(request):
#     bbf = BbForm()
#     rubrics = Rubric.objects.all()
#     context = {'form': bbf,  'rubrics': rubrics}
#     return render(request, 'bboard/create.html', context)
#
#
# def add_save(request):
#     bbf = BbForm(request.POST)
#     if bbf.is_valid():
#         return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
#     else:
#         context = {'form': bbf}
#         return render(request, 'bboard/create.html', context)



# name: это строка которую транслитим
# def transliterate(name):
#     """
#     Автор: LarsKort
#     Дата: 16/07/2011; 1:05 GMT-4;
#     Не претендую на "хорошесть" словарика. В моем случае и такой пойдет,
#     вы всегда сможете добавить свои символы и даже слова. Только
#     это нужно делать в обоих списках, иначе будет ошибка.
#     """
#     # Слоаврь с заменами
#     slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
#               'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
#               'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
#               'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
#               'ю': 'u', 'я': 'ja', 'А': 'a', 'Б': 'b', 'В': 'v', 'Г': 'g', 'Д': 'd', 'Е': 'e', 'Ё': 'e',
#               'Ж': 'zh', 'З': 'z', 'И': 'i', 'Й': 'i', 'К': 'k', 'Л': 'l', 'М': 'm', 'Н': 'n',
#               'О': 'o', 'П': 'p', 'Р': 'r', 'С': 's', 'Т': 't', 'У': 'u', 'Ф': 'Х', 'х': 'h',
#               'Ц': 'c', 'Ч': 'cz', 'Ш': 'sh', 'Щ': 'scz', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'e',
#               'Ю': 'u', 'Я': 'ja', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
#               '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
#               ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
#               '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
#               'Є': 'e'}
#
#     # Циклически заменяем все буквы в строке
#     for key in slovar:
#         name = name.replace(key, slovar[key])
#     return name
