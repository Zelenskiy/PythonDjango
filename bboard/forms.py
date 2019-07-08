
from django.forms import ModelForm, TextInput

from .models import Bb


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = {'title', 'content', 'price', 'slug', 'rubric'}
        widgets = {
            'slug': TextInput(attrs={'class': 'colortext'}),
        }

