from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import datetime, timedelta
from vendas.models import Venda, ItemVenda
from produtos.models import Produto
from clientes.models import Cliente

@login_required
def dashboard(request):
    hoje = timezone.now().date()
    mes_atual = hoje.replace(day=1)
    
    vendas_hoje = Venda.objects.filter(
        data_venda__date=hoje,
        status='C'
    ).aggregate(
        total=Sum('total'),
        quantidade=Count('id')
    )
    
    vendas_mes = Venda.objects.filter(
        data_venda__date__gte=mes_atual,
        status='C'
    ).aggregate(
        total=Sum('total'),
        quantidade=Count('id')
    )
    
    produtos_baixo_estoque = Produto.objects.filter(
        ativo=True,
        estoque_atual__lte=F('estoque_minimo')
    ).count()
    
    total_clientes = Cliente.objects.filter(ativo=True).count()
    
    ultimas_vendas = Venda.objects.filter(status='C').order_by('-data_venda')[:5]
    
    context = {
        'vendas_hoje': vendas_hoje,
        'vendas_mes': vendas_mes,
        'produtos_baixo_estoque': produtos_baixo_estoque,
        'total_clientes': total_clientes,
        'ultimas_vendas': ultimas_vendas,
    }
    return render(request, 'relatorios/dashboard.html', context)

@login_required
def relatorio_vendas(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    vendas = Venda.objects.filter(status='C')
    
    if data_inicio:
        vendas = vendas.filter(data_venda__date__gte=data_inicio)
    if data_fim:
        vendas = vendas.filter(data_venda__date__lte=data_fim)
    
    resumo = vendas.aggregate(
        total_vendas=Sum('total'),
        quantidade_vendas=Count('id'),
        ticket_medio=Sum('total') / Count('id') if vendas.exists() else 0
    )
    
    context = {
        'vendas': vendas,
        'resumo': resumo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }
    return render(request, 'relatorios/vendas.html', context)

@login_required
def relatorio_estoque(request):
    produtos = Produto.objects.filter(ativo=True)
    
    produtos_vendidos = ItemVenda.objects.values('produto__nome').annotate(
        total_vendido=Sum('quantidade')
    ).order_by('-total_vendido')[:10]
    
    context = {
        'produtos': produtos,
        'produtos_vendidos': produtos_vendidos,
    }
    return render(request, 'relatorios/estoque.html', context)
