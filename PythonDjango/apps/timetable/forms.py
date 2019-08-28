from django.forms import ModelForm, Textarea, TextInput, Select, CheckboxInput
from django import forms

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from timetable.models import Teacher
from worktime.models import Settings, Vacat, Workday, Missing, Academyear, Worktimetable, Hourlyworker


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = {'name',
                  'short',
                  'gender',
                  'color',
                  'sort',
                  'timetable_id'
                  }
        widgets = {
            # 'teach': Select(attrs={'id': 'teacher', 'class': 'form-control'}),
            # 'date_st': TextInput(attrs={'id': 'datepicker1', 'name': 'datepicker1', 'class': 'form-control'}),
            # 'date_fin': TextInput(attrs={'id': 'datepicker2', 'name': 'datepicker2', 'class': 'form-control'}),
            # 'reason': TextInput(attrs={'id': 'reason', 'name': 'reason', 'class': 'form-control', 'onkeyup': 'reasType();', 'onfocus': 'reasEnter();'}),
            #
            #
            #
            # 'worktimeable': TextInput(attrs={'id': 'workttlist'}),
        }


