from django.urls import path
from .views import index, by_rubric, post_detail, edit, add, Post_delete

urlpatterns = [

    path('add/', add, name='add'),

    path('edit/<str:slug>/', edit, name='edit_url'),
    path('delete/<str:slug>/', Post_delete.as_view(), name='post_delete_url'),

    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
    path('<str:slug>/', post_detail, name='post_detail_url'),

]
