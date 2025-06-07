from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Produto, Categoria

@login_required
def lista_produtos(request):
    search = request.GET.get('search', '')
    categoria_id = request.GET.get('categoria', '')
    
    produtos = Produto.objects.filter(ativo=True)
    
    if search:
        produtos = produtos.filter(
            Q(nome__icontains=search) | 
            Q(codigo__icontains=search) | 
            Q(codigo_barras__icontains=search)
        )
    
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    
    categorias = Categoria.objects.filter(ativo=True)
    
    context = {
        'produtos': produtos,
        'categorias': categorias,
        'search': search,
        'categoria_selecionada': categoria_id,
    }
    return render(request, 'produtos/lista.html', context)

@login_required
def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produtos/detalhe.html', {'produto': produto})
