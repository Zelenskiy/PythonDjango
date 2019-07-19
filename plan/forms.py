from django.forms import ModelForm, Textarea
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from plan.models import Plan
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = {'id', 'content', 'termin', 'generalization', 'responsible', 'note', 'sort', \
                  'direction_id', 'purpose_id', 'show', 'done'}
        widgets = {
            'content': Textarea(attrs={'rows': '4'}),
            # 'content': forms.Textarea({'class': 'form-control'}),
            # 'termin': forms.TextInput({'class': 'form-control'}),
            # 'generalization': forms.TextInput({'class': 'form-control'}),
            # 'responsible': forms.TextInput({'class': 'form-control'}),
            # 'note': forms.TextInput({'class': 'form-control'}),
        }



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
