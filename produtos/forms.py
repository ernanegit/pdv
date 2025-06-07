# produtos/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Produto, Categoria

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'codigo', 'nome', 'descricao', 'categoria', 'imagem',
            'preco_custo', 'preco_venda', 'estoque_atual', 'estoque_minimo',
            'unidade_medida', 'codigo_barras', 'ativo'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'imagem': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'help_text': 'Formatos aceitos: JPG, PNG, WEBP (Max: 2MB)'
            }),
            'preco_custo': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'preco_venda': forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
            'estoque_atual': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'unidade_medida': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }