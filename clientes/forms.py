from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome', 'tipo_pessoa', 'cpf_cnpj', 'email', 'telefone',
            'data_nascimento', 'endereco', 'numero', 'complemento',
            'bairro', 'cidade', 'uf', 'cep', 'observacoes', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_pessoa': forms.Select(attrs={'class': 'form-select'}),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CPF ou CNPJ'
            }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Selecione...'),
                ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'AmapÃ¡'),
                ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'CearÃ¡'),
                ('DF', 'Distrito Federal'), ('ES', 'EspÃ­rito Santo'),
                ('GO', 'GoiÃ¡s'), ('MA', 'MaranhÃ£o'), ('MT', 'Mato Grosso'),
                ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                ('PA', 'ParÃ¡'), ('PB', 'ParaÃ­ba'), ('PR', 'ParanÃ¡'),
                ('PE', 'Pernambuco'), ('PI', 'PiauÃ­'), ('RJ', 'Rio de Janeiro'),
                ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
                ('RO', 'RondÃ´nia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                ('SP', 'SÃ£o Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
            ]),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000'
            }),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
