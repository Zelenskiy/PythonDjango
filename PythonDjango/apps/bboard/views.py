import os

from django.conf.urls import url
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import View

from PythonDjango.settings import MEDIA_DIR
from .models import Bb, Rubric, Albom
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from .forms import BbForm
from django import forms
import PIL
from PIL import Image
# from .utils import *
from django.urls import reverse


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


# class BbCreateView(CreateView):
#     template_name = 'bboard/add.html'
#     form_class = BbForm
#     success_url = reverse_lazy('index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['rubrics'] = Rubric.objects.all()
#         return context

# def add(ObjectCreateMixin):
#     model_form = BbForm
#     template = 'bboard/add.html'

class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        print(context)
        return context
    # def form_valid(self, form):
    #     return super(BbForm, self).form_valid(form)


def add(request):
    post = Bb(title='', content='', price='')
    form = BbForm(request.POST, request.FILES)
    if request.method == "POST":
        if form.is_valid():
            if 'photo' in request.FILES:
                # form.photo = request.FILES['photo']
                form.photo_prev = request.FILES['photo']
                # form.photo_ori = request.FILES['photo']
                handle_uploaded_file(request.FILES['photo'])
            post = form.save(commit=False)
            post.moder = 0
            post.save()
            # if 'photo' in request.FILES:
            #     resize_for_prev(form.photo)
            return redirect('../')
    else:
        # pass
        form = BbForm(instance=post)
    return render(request, 'bboard/create.html', {'form': form})


def add_and_save(request):
    if request.method == "POST":
        bbf = BbForm(request.POST, request.FILES)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('bboard:by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)

# TODO
def handle_uploaded_file(f):
    with open('d:/name.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


class Post_delete(View):
    def get(self, request, slug):
        post = Bb.objects.get(slug__iexact=slug)
        return render(request, 'bboard/post_delete.html', context={'post': post})

    def post(self, request, slug):
        post = Bb.objects.get(slug__iexact=slug)
        post.delete()
        return redirect(reverse('index'))


def post_detail(request, slug):
    post = Bb.objects.get(slug__iexact=slug)
    # images = Albom.objects.all()
    albom = Albom.objects.filter(bb__slug__iexact=slug)
    return render(request, 'bboard/post_detail.html', context={'post': post, 'albom': albom})


def resize_for_prev(photo):
    baseheight = 150
    img = Image.open(os.path.join(MEDIA_DIR, 'user_images', str(photo)))
    hpercent = (baseheight / float(img.size[1]))
    wsize = int((float(img.size[0]) * float(hpercent)))
    img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
    img.save(os.path.join(MEDIA_DIR, 'prev_user_images', str(photo)))

# def edit(request, slug):
#     # post = get_object_or_404(Bb, slug__iexact=slug)
#     post = Bb.objects.get(slug__iexact=slug)
#     if request.method == "POST":
#         form = BbForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             if 'photo' in request.FILES:
#                 form.photo = request.FILES['photo']
#                 form.photo_prev = request.FILES['photo']
#                 # form.photo_prev = os.path.join('user_photo_prev', str(form.photo))
#                 handle_uploaded_file(request.FILES['photo'])
#             post = form.save(commit=False)
#             # К примеру меняем одно поле сами, если не нужно, то просто сохраняем
#             post.moder = 0
#             post.save()
#             # if 'photo' in request.FILES:
#             #     resize_for_prev(post.photo)
#             return redirect('../../')
#     else:
#         form = BbForm(instance=post)
#     return render(request, 'bboard/edit.html', {'form': form})

# def add(request):
#     bbf = BbForm()
#     rubrics = Rubric.objects.all()
#     context = {'form': bbf,  'rubrics': rubrics}
#     return render(request, 'bboard/add.html', context)
#
#
# def add_save(request):
#     bbf = BbForm(request.POST)
#     if bbf.is_valid():
#         return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
#     else:
#         context = {'form': bbf}
#         return render(request, 'bboard/add.html', context)


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
