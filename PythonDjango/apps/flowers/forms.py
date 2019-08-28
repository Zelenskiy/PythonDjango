from django import forms
from flowers.models import SimpleAddFlower

class SimpleAddFlowerForm(forms.ModelForm):
    class Meta:
        model = SimpleAddFlower
        fields = ('title', 'description', 'care', 'photo')

