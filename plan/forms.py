from django.forms import ModelForm, Textarea

from plan.models import Plan
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm

class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = {'id', 'content', 'termin', 'generalization', 'responsible', 'note', 'sort', \
                  'direction_id', 'purpose_id', 'show', 'done'}
        widgets = {
            'content': Textarea(attrs={'rows': '6'}),
        }

class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)
