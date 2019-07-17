from django.contrib import admin

from django.contrib import admin

from .models import *




class PlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'termin', 'generalization', 'responsible', 'note', 'sort', \
                  'direction_id', 'purpose_id', 'show', 'done')
    list_display_links = ('responsible', 'content')
    search_fields = ('title', 'content')


admin.site.register(Plan)
admin.site.register(Rubric)

