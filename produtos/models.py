from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

class Categoria(models.Model):
    nome = models.CharField(_('Nome'), max_length=100, unique=True)
    descricao = models.TextField(_('DescriÃ§Ã£o'), blank=True)
    ativo = models.BooleanField(_('Ativo'), default=True)
    criado_em = models.DateTimeField(_('Criado em'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Categoria')
        verbose_name_plural = _('Categorias')
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Produto(models.Model):
    codigo = models.CharField(_('CÃ³digo'), max_length=50, unique=True)
    nome = models.CharField(_('Nome'), max_length=200)
    descricao = models.TextField(_('DescriÃ§Ã£o'), blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name=_('Categoria'))
    preco_custo = models.DecimalField(_('PreÃ§o de Custo'), max_digits=10, decimal_places=2, default=0)
    preco_venda = models.DecimalField(_('PreÃ§o de Venda'), max_digits=10, decimal_places=2)
    estoque_atual = models.IntegerField(_('Estoque Atual'), default=0)
    estoque_minimo = models.IntegerField(_('Estoque MÃ­nimo'), default=0)
    unidade_medida = models.CharField(_('Unidade de Medida'), max_length=10, default='UN')
    codigo_barras = models.CharField(_('CÃ³digo de Barras'), max_length=50, blank=True)
    ativo = models.BooleanField(_('Ativo'), default=True)
    criado_em = models.DateTimeField(_('Criado em'), auto_now_add=True)
    atualizado_em = models.DateTimeField(_('Atualizado em'), auto_now=True)
    
    class Meta:
        verbose_name = _('Produto')
        verbose_name_plural = _('Produtos')
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}"
    
    @property
    def margem_lucro(self):
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0
    
    @property
    def estoque_baixo(self):
        return self.estoque_atual <= self.estoque_minimo
