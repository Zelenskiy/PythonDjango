from django.forms import ModelForm, Textarea

from plan.models import Plan


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = {'content', 'termin', 'generalization', 'responsible', 'note', 'sort', \
                  'direction_id', 'purpose_id', 'show', 'done'}
        widgets = {
            'content': Textarea(attrs={'rows': '6'}),
        }
