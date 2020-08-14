from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('submit/', views.submit, name='submit'),
    path('get_pass/', views.get_pass, name='get_pass'),
]