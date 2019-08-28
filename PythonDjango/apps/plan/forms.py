from django.forms import ModelForm, Textarea, TextInput
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
            'content': Textarea(attrs={'rows': '7', 'placeholder': 'Впишіть сюди зміст заходу'}),
            'termin': TextInput(attrs={'placeholder': 'Впишіть сюди дату чи період',  'class': 'form-control'}),
            'responsible': TextInput(attrs={ 'placeholder': 'Впишіть сюди відповідального за захід',  'class': 'form-control'}),
            'generalization': TextInput(attrs={ 'placeholder': 'Впишіть сюди документ, у якому захід узагальниться',  'class': 'form-control'}),


            # 'content': forms.Textarea({'class': 'form-control'}),
            # 'termin': forms.TextInput({'class': 'form-control'}),
            # 'generalization': forms.TextInput({'class': 'form-control'}),
            # 'responsible': forms.TextInput({'class': 'form-control'}),
            # 'note': forms.TextInput({'class': 'form-control'}),
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
