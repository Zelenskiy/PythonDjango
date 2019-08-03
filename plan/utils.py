from django.db.models import Max
from django.shortcuts import get_object_or_404, render, redirect

# class ObjectDetailMixin:
#     model = None
#     template = None
#
#     def get(self, request, slug):
#         obj = get_object_or_404(self.model, slug__iexact=slug)
#         return render(request, self.template, content={self.model.__name__.lower(): obj})
#
# class ObjectCreateMixin:
#     model_form = None
#     template = None
#
#     def gen(self, request):
#         form = self.model_form()
#         return render(request, self.template, content={'form': form})
#
#     def post(self, request):
#         bound_form = self.model_form(request.POST)
#         if bound_form.is_valid():
#             new_obj = bound_form.save()
#             return redirect(new_obj)
#         return render(request, self.template, content={'form': bound_form})


# Експорт плану у Word


# Формування дерева розділів
from plan.models import Rubric, Plantable
from worktime.models import Settings


# def tree(r):
#
#
#     return 1

def rubric_tree():
    r_tree = {}
    s = Settings.objects.filter(field='plantable')[0].value
    table = Plantable.objects.get(pk=int(s))

    rubrics = Rubric.objects.filter(plantable_id=table)

    # max_id = Rubric.objects.aggregate(Max('id'))
    i = 0
    for rubric in rubrics:
        if rubric.riven == 1:
            child = {}
            child['text'] = (str(rubric.n_r) + '. ' + rubric.name)
            child['riven'] = 1
            child['n_r'] = rubric.n_r
            child['r_id'] = rubric.id
            r_tree[i] = child
            i += 1
            for rubric2 in rubrics:
                if rubric2.riven == 2 and rubric2.id_owner_id == rubric.id:
                    child = {}
                    child['text'] = (str(rubric.n_r) + '. ' +str(rubric2.n_r) + '. ' + rubric2.name)
                    child['riven'] = 2
                    child['r_id'] = rubric2.id
                    r_tree[i] = child
                    i += 1
                    for rubric3 in rubrics:
                        if rubric3.riven == 3 and rubric3.id_owner_id == rubric2.id:
                            child = {}
                            child['text'] = (str(rubric.n_r) + '. ' + str(rubric2.n_r) + '. ' +str(rubric3.n_r) + '. ' + rubric3.name)
                            child['riven'] = 3
                            child['r_id'] = rubric3.id
                            r_tree[i] = child
                            i += 1
    count_r = i
    return r_tree


"""
{ %
for rubric in rubrics %}
{ % if rubric.riven == 1 %}
< option
id = "{{ rubric.id }}"
owner = "{{ rubric.id_owner_id }}"
hidden_child = true
r = "0" >
{{rubric.n_r}}. & nbsp;
{{rubric.name}}
< / option >
{ %
for rubric2 in rubrics %}
{ % if rubric2.riven == 2 and rubric2.id_owner_id == rubric.id %}
< option
id = "{{ rubric2.id }}"
owner = "{{ rubric2.id_owner_id }}"
hidden_child = true
r = "0" >
& nbsp; & nbsp;
{{rubric.n_r}}. & nbsp;
{{rubric2.n_r}}. & nbsp;
{{rubric2.name}}
< / option >

{ %
for rubric3 in rubrics %}
{ % if rubric3.riven == 3 and rubric3.id_owner_id == rubric2.id %}
< option
id = "{{ rubric3.id }}"
owner = "{{ rubric3.id_owner_id }}"
hidden_child = true
r = "0" >
& nbsp; & nbsp;
& nbsp; & nbsp;
{{rubric.n_r}}. & nbsp;
{{rubric2.n_r}}. & nbsp;
{{rubric3.n_r}}. & nbsp;
{{rubric3.name}}
< / option >
{ % endif %}
{ % endfor %}
{ % endif %}
{ % endfor %}
{ % endif %}
{ % endfor %}
"""
