from django.forms import ModelForm

from plan.models import Plan


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = {'content', 'termin', 'generalization', 'responsible', 'note', 'sort', \
                  'direction_id', 'purpose_id', 'show', 'done'}
        widgets = {
            # 'slug': TextInput(attrs={'class': 'colortext'}),
        }