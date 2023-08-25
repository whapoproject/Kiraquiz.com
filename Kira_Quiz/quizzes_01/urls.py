from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_view_01, name='quiz_view_01'),
    path('results_01/', views.results_01, name='results_01'),
]
