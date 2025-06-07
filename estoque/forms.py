from django import forms
from django.utils.translation import gettext_lazy as _
from produtos.models import Produto

class MovimentacaoEstoqueForm(forms.Form):
    TIPO_CHOICES = [
        ('entrada', _('Entrada')),
        ('saida', _('SaÃ­da')),
    ]
    
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.filter(ativo=True),
        label=_('Produto'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        label=_('Tipo de MovimentaÃ§Ã£o'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantidade = forms.IntegerField(
        label=_('Quantidade'),
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    motivo = forms.CharField(
        label=_('Motivo'),
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Descreva o motivo da movimentaÃ§Ã£o...'
        })
    )

class FiltroEstoqueForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar produto...',
            'class': 'form-control'
        })
    )
    apenas_baixo = forms.BooleanField(
        required=False,
        label=_('Apenas produtos com estoque baixo'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
