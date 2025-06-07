from django.urls import path
from . import views

app_name = 'vendas'

urlpatterns = [
    path('', views.lista_vendas, name='lista'),
    path('nova/', views.nova_venda, name='nova'),
    path('pdv/', views.pdv_view, name='pdv'),
    path('<int:pk>/', views.detalhe_venda, name='detalhe'),
    path('ajax/buscar-produto/', views.buscar_produto_ajax, name='buscar_produto_ajax'),
]
