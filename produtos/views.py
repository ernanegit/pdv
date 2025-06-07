from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, F
from django.urls import reverse
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm

@login_required
def lista_produtos(request):
    search = request.GET.get('search', '')
    categoria_id = request.GET.get('categoria', '')
    apenas_baixo = request.GET.get('apenas_baixo', False)
    
    produtos = Produto.objects.filter(ativo=True)
    
    if search:
        produtos = produtos.filter(
            Q(nome__icontains=search) | 
            Q(codigo__icontains=search) | 
            Q(codigo_barras__icontains=search)
        )
    
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)
    
    if apenas_baixo:
        produtos = produtos.filter(estoque_atual__lte=F('estoque_minimo'))
    
    categorias = Categoria.objects.filter(ativo=True)
    
    context = {
        'produtos': produtos,
        'categorias': categorias,
        'search': search,
        'categoria_selecionada': categoria_id,
        'apenas_baixo': apenas_baixo,
    }
    return render(request, 'produtos/lista.html', context)

@login_required
def detalhe_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'produtos/detalhe.html', {'produto': produto})

@login_required
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto "{produto.nome}" criado com sucesso!')
            return redirect('produtos:detalhe', pk=produto.pk)
    else:
        form = ProdutoForm()
    
    context = {
        'form': form,
        'titulo': 'Novo Produto',
        'action': 'Criar',
        'voltar_url': reverse('produtos:lista'),
    }
    return render(request, 'produtos/form.html', context)

@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto "{produto.nome}" atualizado com sucesso!')
            return redirect('produtos:detalhe', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)
    
    context = {
        'form': form,
        'produto': produto,
        'titulo': f'Editar Produto: {produto.nome}',
        'action': 'Atualizar',
        'voltar_url': reverse('produtos:detalhe', kwargs={'pk': produto.pk}),
    }
    return render(request, 'produtos/form.html', context)

@login_required
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    
    if request.method == 'POST':
        nome_produto = produto.nome
        produto.ativo = False  # Soft delete
        produto.save()
        messages.success(request, f'Produto "{nome_produto}" removido com sucesso!')
        return redirect('produtos:lista')
    
    context = {
        'produto': produto,
        'titulo': f'Remover Produto: {produto.nome}',
    }
    return render(request, 'produtos/confirmar_delete.html', context)

# Views para Categorias
@login_required
def lista_categorias(request):
    categorias = Categoria.objects.filter(ativo=True).order_by('nome')
    return render(request, 'produtos/categorias.html', {'categorias': categorias})

@login_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria "{categoria.nome}" criada com sucesso!')
            return redirect('produtos:categorias')
    else:
        form = CategoriaForm()
    
    context = {
        'form': form,
        'titulo': 'Nova Categoria',
        'action': 'Criar',
        'voltar_url': reverse('produtos:categorias'),
    }
    return render(request, 'produtos/categoria_form.html', context)

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoria "{categoria.nome}" atualizada com sucesso!')
            return redirect('produtos:categorias')
    else:
        form = CategoriaForm(instance=categoria)
    
    context = {
        'form': form,
        'categoria': categoria,
        'titulo': f'Editar Categoria: {categoria.nome}',
        'action': 'Atualizar',
        'voltar_url': reverse('produtos:categorias'),
    }
    return render(request, 'produtos/categoria_form.html', context)