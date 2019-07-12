import os
from time import time

from PIL import Image
from django.db import models


# Create your models here.
from django.utils.text import slugify

from PythonDjango.settings import MEDIA_DIR


def gen_slug(s):
    return slugify(s, allow_unicode=True) + '-' + str(int(time()))

class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Опис')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    slug = models.SlugField(null=False, max_length=150, unique=True, default="", verbose_name='Slug')
    photo = models.CharField(max_length=250, blank=True, null=True)
    photo_prev = models.ImageField(upload_to='', blank=True, null=True)
    photo_ori = models.ImageField(upload_to='user_images', blank=True, null=True)
    def gen_slug(s):
        return slugify(s, allow_unicode=True)+'-'+str(int(time()))

    def save(self, *args, **kwargs):
        # if not self.id and not self.photo_prev:
        #     return
        if not self.id:
            self.slug = gen_slug(self.title)
        super(Bb, self).save(*args, **kwargs)
        image = Image.open(self.photo_prev)
        (width, height) = image.size
        # "Max width and height 250"
        if (250 / width < 250 / height):
            factor = 250 / height
        else:
            factor = 250 / width
        size = (int(width / factor), int(height / factor))
        image_prev = image.resize(size, Image.ANTIALIAS)
        image_prev.save(self.photo_prev.path)
        # image.save(self.photo_ori.path)
        file_name = os.path.basename(str(self.photo_prev.path))
        # self.photo = file_name
        image.save(os.path.join(MEDIA_DIR, 'user_images', file_name))


        # image.save(self.photo.path)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']

#TODO
def handle_uploaded_file(f):
    with open('d:/name.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Назва')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

class Albom(models.Model):
    content = models.TextField(null=True, blank=True, verbose_name='Опис')
    image = models.ImageField(upload_to='user_images', blank=True, null=True)
    bb = models.ForeignKey('Bb', null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = 'Малюнок'
        verbose_name = 'Малюнки'
        ordering = ['content']