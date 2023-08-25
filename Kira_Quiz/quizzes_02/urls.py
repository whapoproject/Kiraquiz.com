from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_view_02, name='quiz_view_02'),
    path('results_02/', views.results_02, name='results_02'),
]
