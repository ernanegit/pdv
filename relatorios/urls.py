from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('vendas/', views.relatorio_vendas, name='vendas'),
    path('estoque/', views.relatorio_estoque, name='estoque'),
]
