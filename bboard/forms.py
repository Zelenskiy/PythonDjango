from django.forms import ModelForm, TextInput, forms

from .models import Bb


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = {'title', 'content', 'price', 'slug', 'rubric', 'photo'}
        widgets = {
            'slug': TextInput(attrs={'class': 'colortext'}),
        }
