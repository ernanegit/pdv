from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.db import transaction
from .models import Venda, ItemVenda
from produtos.models import Produto
from clientes.models import Cliente
import json

@login_required
def lista_vendas(request):
    search = request.GET.get('search', '')
    vendas = Venda.objects.all()
    
    if search:
        vendas = vendas.filter(
            Q(numero_venda__icontains=search) |
            Q(cliente__nome__icontains=search)
        )
    
    context = {
        'vendas': vendas,
        'search': search,
    }
    return render(request, 'vendas/lista.html', context)

@login_required
def detalhe_venda(request, pk):
    venda = get_object_or_404(Venda, pk=pk)
    return render(request, 'vendas/detalhe.html', {'venda': venda})

@login_required
def pdv_view(request):
    produtos = Produto.objects.filter(ativo=True, estoque_atual__gt=0)
    clientes = Cliente.objects.filter(ativo=True)
    
    context = {
        'produtos': produtos,
        'clientes': clientes,
    }
    return render(request, 'vendas/pdv.html', context)

@login_required
def nova_venda(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                cliente_id = request.POST.get('cliente_id')
                forma_pagamento = request.POST.get('forma_pagamento', 'D')
                desconto = float(request.POST.get('desconto', 0))
                observacoes = request.POST.get('observacoes', '')
                
                itens_json = request.POST.get('itens')
                itens = json.loads(itens_json) if itens_json else []
                
                if not itens:
                    messages.error(request, 'Adicione pelo menos um item Ã  venda.')
                    return redirect('vendas:pdv')
                
                venda = Venda.objects.create(
                    cliente_id=cliente_id if cliente_id else None,
                    vendedor=request.user,
                    forma_pagamento=forma_pagamento,
                    desconto=desconto,
                    observacoes=observacoes,
                    status='C'
                )
                
                subtotal = 0
                for item in itens:
                    produto = Produto.objects.get(pk=item['produto_id'])
                    quantidade = float(item['quantidade'])
                    preco_unitario = float(item['preco_unitario'])
                    
                    if produto.estoque_atual < quantidade:
                        raise ValueError(f'Estoque insuficiente para {produto.nome}')
                    
                    ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=quantidade,
                        preco_unitario=preco_unitario,
                        subtotal=quantidade * preco_unitario
                    )
                    
                    produto.estoque_atual -= int(quantidade)
                    produto.save()
                    
                    subtotal += quantidade * preco_unitario
                
                venda.subtotal = subtotal
                venda.total = subtotal - desconto
                venda.save()
                
                messages.success(request, f'Venda {venda.numero_venda} realizada com sucesso!')
                return redirect('vendas:detalhe', pk=venda.pk)
                
        except Exception as e:
            messages.error(request, f'Erro ao processar venda: {str(e)}')
            return redirect('vendas:pdv')
    
    return redirect('vendas:pdv')

@login_required
def buscar_produto_ajax(request):
    term = request.GET.get('term', '')
    produtos = Produto.objects.filter(
        Q(nome__icontains=term) | Q(codigo__icontains=term),
        ativo=True,
        estoque_atual__gt=0
    )[:10]
    
    results = []
    for produto in produtos:
        results.append({
            'id': produto.id,
            'codigo': produto.codigo,
            'nome': produto.nome,
            'preco': str(produto.preco_venda),
            'estoque': produto.estoque_atual,
        })
    
    return JsonResponse(results, safe=False)
