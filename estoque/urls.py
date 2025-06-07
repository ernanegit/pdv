from django.urls import path
from . import views

app_name = 'estoque'

urlpatterns = [
    path('', views.lista_estoque, name='lista'),
    path('movimentacao/', views.movimentacao_estoque, name='movimentacao'),
]
