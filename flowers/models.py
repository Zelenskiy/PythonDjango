from django.db import models


class SimpleAddFlower(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    care = models.TextField()
    photo = models.ImageField(upload_to='q1', blank=True, null=True)
