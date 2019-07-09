from django.urls import path
from .views import index, by_rubric, BbCreateView, post_detail, edit


urlpatterns = [

    path('add/', BbCreateView.as_view(), name='add'),
    # path('edit/', edit, name='edit_url'),
    path('edit/<str:slug>/', edit, name='edit_url'),
    #
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
    path('<str:slug>/', post_detail, name='post_detail_url'),

]
