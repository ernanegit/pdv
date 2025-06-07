from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    # Produtos
    path('', views.lista_produtos, name='lista'),
    path('novo/', views.criar_produto, name='criar'),
    path('<int:pk>/', views.detalhe_produto, name='detalhe'),
    path('<int:pk>/editar/', views.editar_produto, name='editar'),
    path('<int:pk>/deletar/', views.deletar_produto, name='deletar'),
    
    # Categorias
    path('categorias/', views.lista_categorias, name='categorias'),
    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
]