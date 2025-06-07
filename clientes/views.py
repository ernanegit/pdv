from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Cliente

@login_required
def lista_clientes(request):
    search = request.GET.get('search', '')
    clientes = Cliente.objects.filter(ativo=True)
    
    if search:
        clientes = clientes.filter(
            Q(nome__icontains=search) |
            Q(cpf_cnpj__icontains=search) |
            Q(email__icontains=search) |
            Q(telefone__icontains=search)
        )
    
    context = {
        'clientes': clientes,
        'search': search,
    }
    return render(request, 'clientes/lista.html', context)

@login_required
def detalhe_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    vendas = cliente.venda_set.all()[:10]
    
    context = {
        'cliente': cliente,
        'vendas': vendas,
    }
    return render(request, 'clientes/detalhe.html', context)
