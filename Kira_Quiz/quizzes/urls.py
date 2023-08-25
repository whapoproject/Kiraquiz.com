from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_view, name='quiz_view'),
    path('results/', views.results, name='results'),
]
