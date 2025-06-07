﻿from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.lista_produtos, name='lista'),
    path('<int:pk>/', views.detalhe_produto, name='detalhe'),
]
