# vendas/views.py - Versão atualizada com integração real do PDV
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Venda, ItemVenda
from produtos.models import Produto, Categoria
from clientes.models import Cliente

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
    produtos = Produto.objects.filter(ativo=True)
    categorias = Categoria.objects.filter(ativo=True)
    clientes = Cliente.objects.filter(ativo=True)
    
    context = {
        'produtos': produtos,
        'categorias': categorias,
        'clientes': clientes,
    }
    return render(request, 'vendas/pdv.html', context)

@login_required
@require_POST
def nova_venda(request):
    try:
        # Parse do JSON ou form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = {
                'cliente_id': request.POST.get('cliente_id'),
                'forma_pagamento': request.POST.get('forma_pagamento', 'D'),
                'desconto': float(request.POST.get('desconto', 0)),
                'observacoes': request.POST.get('observacoes', ''),
                'itens': json.loads(request.POST.get('itens', '[]'))
            }
        
        with transaction.atomic():
            cliente_id = data.get('cliente_id')
            forma_pagamento = data.get('forma_pagamento', 'D')
            desconto = float(data.get('desconto', 0))
            observacoes = data.get('observacoes', '')
            itens = data.get('itens', [])
            
            if not itens:
                return JsonResponse({
                    'success': False,
                    'error': 'Adicione pelo menos um item à venda.'
                })
            
            # Criar a venda
            venda = Venda.objects.create(
                cliente_id=cliente_id if cliente_id else None,
                vendedor=request.user,
                forma_pagamento=forma_pagamento,
                desconto=desconto,
                observacoes=observacoes,
                status='C'
            )
            
            subtotal = 0
            
            # Processar cada item
            for item_data in itens:
                try:
                    produto = Produto.objects.get(pk=item_data['produto_id'])
                    quantidade = int(item_data['quantidade'])
                    preco_unitario = float(item_data['preco_unitario'])
                    
                    # Verificar estoque
                    if produto.estoque_atual < quantidade:
                        raise ValueError(f'Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque_atual}')
                    
                    # Criar item da venda
                    item_venda = ItemVenda.objects.create(
                        venda=venda,
                        produto=produto,
                        quantidade=quantidade,
                        preco_unitario=preco_unitario,
                        subtotal=quantidade * preco_unitario
                    )
                    
                    # Atualizar estoque
                    produto.estoque_atual -= quantidade
                    produto.save()
                    
                    subtotal += item_venda.subtotal
                    
                except Produto.DoesNotExist:
                    raise ValueError(f'Produto com ID {item_data["produto_id"]} não encontrado')
                except (ValueError, KeyError) as e:
                    raise ValueError(f'Dados inválidos para item: {str(e)}')
            
            # Atualizar totais da venda
            venda.subtotal = subtotal
            venda.total = subtotal - desconto
            venda.save()
            
            return JsonResponse({
                'success': True,
                'numero_venda': venda.numero_venda,
                'total': float(venda.total),
                'message': f'Venda {venda.numero_venda} realizada com sucesso!'
            })
                
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

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

@login_required
def obter_estoque_produto(request, produto_id):
    """View para obter o estoque atual de um produto"""
    try:
        produto = Produto.objects.get(pk=produto_id, ativo=True)
        return JsonResponse({
            'success': True,
            'estoque_atual': produto.estoque_atual,
            'estoque_minimo': produto.estoque_minimo,
            'estoque_baixo': produto.estoque_baixo
        })
    except Produto.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Produto não encontrado'
        })