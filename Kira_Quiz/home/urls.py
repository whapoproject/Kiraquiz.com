from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcomepage, name= 'welcomepage'),
    path('levels/', views.levels, name='levels'),
    path('level_0', views.level_0, name='level_0'),
    path('level_1', views.level_1, name='level_1'),
    path('level_2', views.level_2, name='level_2'),
]