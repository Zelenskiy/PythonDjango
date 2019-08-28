from django.urls import path
from .views import index, by_rubric, post_detail, add, Post_delete, BbEditView, add_and_save

app_name = 'bboard'
urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('addandsave/', add_and_save, name='addandsave'),
    path('edit/<str:slug>/', BbEditView.as_view()),
    # path('edit/<str:slug>/', edit, name='edit_url'),
    path('delete/<str:slug>/', Post_delete.as_view(), name='post_delete_url'),
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),

    path('<str:slug>/', post_detail, name='post_detail_url'),

]
