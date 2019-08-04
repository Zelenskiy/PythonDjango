from django.forms import ModelForm, Textarea, TextInput, Select, CheckboxInput
from django import forms

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from worktime.models import Settings, Vacat, Workday, Missing, Academyear, Worktimetable


class MissForm(ModelForm):
    class Meta:
        model = Missing
        fields = {'teach', 'date_st', 'date_fin', 'reason', 'kl_ker', 'poch_kl', 'worktimeable'}
        widgets = {
            'teach': Select(attrs={'class': 'form-control'}),
            'date_st': TextInput(attrs={'id': 'datepicker1', 'name': 'datepicker1', 'class': 'form-control'}),
            'date_fin': TextInput(attrs={'id': 'datepicker2', 'name': 'datepicker2', 'class': 'form-control'}),
            'reason': TextInput(attrs={'id': 'reason', 'name': 'reason', 'class': 'form-control', 'onkeyup': 'reasType();', 'onfocus': 'reasEnter();'}),
            # 'kl_ker': CheckboxInput(attrs={'class': 'custom-control-checkbox'}),
            # 'poch_kl': CheckboxInput(attrs={'class': 'custom-control-label'}),
            # 'poch_kl': CheckboxInput(attrs={'class': 'form-control'}),



            'worktimeable': TextInput(attrs={'id': 'workttlist'}),
        }
    # CheckboxInput
    # def get_initials(self):
    #     ac = Academyear.objects.get(pk=1)
    #     wt = Worktimetable.objects.filter(acyear_id=ac)[0]
    #
    #
    #     return {
    #         'worktimeable': wt
    #     }


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
