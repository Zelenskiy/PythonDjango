from django.forms import ModelForm, TextInput, forms

from .models import Bb


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = {'title', 'content', 'price', 'rubric', 'photo', 'photo_prev', 'photo_ori'}
        widgets = {
            'slug': TextInput(attrs={'class': 'colortext'}),
        }
