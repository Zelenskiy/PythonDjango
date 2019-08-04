from django.forms import ModelForm, Textarea, TextInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from plan.models import Plan
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

from timetable.models import Teacher
from worktime.models import Settings, Vacat, Workday, Missing


class MissForm(ModelForm):
    class Meta:
        model = Missing
        fields = {'teach', 'date_st', 'date_fin', 'reason', 'kl_ker', 'poch_kl'}


class SettingsForm(ModelForm):
    class Meta:
        model = Settings
        fields = {'field', 'value'}
        widgets = {
        }


class VacationForm(ModelForm):
    class Meta:
        model = Vacat
        fields = {'date', 'name', 'deleted'}
        widgets = {
            'date': TextInput(attrs={'placeholder': 'dd.mm.yyyy', 'class': 'form-control'}),
            'name': TextInput(attrs={'placeholder': 'Впишіть сюди свято', 'class': 'form-control'}),
        }


class WorkdayForm(ModelForm):
    class Meta:
        model = Workday
        fields = {'num', 'wday', 'numworkweek', 'dayweek', 'weekchzn'}

        widgets = {

        }


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput)
    first_name = forms.CharField(label="Ім'я", widget=forms.TextInput)
    email = forms.CharField(label='Електронна пошта', widget=forms.EmailInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль повторно', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароль не співпадає')
        return cd['password2']
