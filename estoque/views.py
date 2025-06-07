from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from produtos.models import Produto

@login_required
def lista_estoque(request):
    search = request.GET.get('search', '')
    apenas_baixo = request.GET.get('apenas_baixo', False)
    
    produtos = Produto.objects.filter(ativo=True)
    
    if search:
        produtos = produtos.filter(
            Q(nome__icontains=search) |
            Q(codigo__icontains=search)
        )
    
    if apenas_baixo:
        produtos = produtos.filter(estoque_atual__lte=F('estoque_minimo'))
    
    context = {
        'produtos': produtos,
        'search': search,
        'apenas_baixo': apenas_baixo,
    }
    return render(request, 'estoque/lista.html', context)

@login_required
def movimentacao_estoque(request):
    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        tipo = request.POST.get('tipo')
        quantidade = int(request.POST.get('quantidade', 0))
        motivo = request.POST.get('motivo', '')
        
        try:
            produto = Produto.objects.get(pk=produto_id)
            
            if tipo == 'entrada':
                produto.estoque_atual += quantidade
            elif tipo == 'saida':
                if produto.estoque_atual >= quantidade:
                    produto.estoque_atual -= quantidade
                else:
                    messages.error(request, 'Quantidade insuficiente em estoque!')
                    return redirect('estoque:movimentacao')
            
            produto.save()
            messages.success(request, f'MovimentaÃ§Ã£o de estoque realizada: {tipo} de {quantidade} unidades.')
            return redirect('estoque:lista')
            
        except Produto.DoesNotExist:
            messages.error(request, 'Produto nÃ£o encontrado!')
    
    produtos = Produto.objects.filter(ativo=True)
    return render(request, 'estoque/movimentacao.html', {'produtos': produtos})
