# setup_pdv.ps1 - Script de configuração para Windows
# Execute: .\setup_pdv.ps1

Write-Host "🚀 === CONFIGURAÇÃO DO SISTEMA PDV (WINDOWS) ===" -ForegroundColor Green
Write-Host ""

# Verificar se está no ambiente virtual
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  ATENÇÃO: Ambiente virtual não detectado!" -ForegroundColor Yellow
    Write-Host "   Recomendamos usar um ambiente virtual:" -ForegroundColor Yellow
    Write-Host "   1. python -m venv venv" -ForegroundColor Cyan
    Write-Host "   2. venv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host ""
}

# 1. Instalar dependências (ignorar Pillow se houver erro)
Write-Host "📦 Instalando dependências..." -ForegroundColor Blue
try {
    pip install Django==4.2.7
    pip install django-crispy-forms==2.0
    pip install crispy-bootstrap5==0.7
    pip install python-decouple==3.8
    
    # Tentar instalar Pillow separadamente
    try {
        pip install Pillow==10.0.1
        Write-Host "✅ Pillow instalado com sucesso" -ForegroundColor Green
    }
    catch {
        Write-Host "⚠️  Pillow não pôde ser instalado - continuando sem ele" -ForegroundColor Yellow
    }
    
    Write-Host "✅ Dependências principais instaladas" -ForegroundColor Green
}
catch {
    Write-Host "❌ Erro na instalação de dependências" -ForegroundColor Red
    exit 1
}

# 2. Criar arquivo .env se não existir
if (-not (Test-Path ".env")) {
    Write-Host "🔧 Criando arquivo .env..." -ForegroundColor Blue
    @"
SECRET_KEY=django-insecure-mude-esta-chave-em-producao-123456789
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ Arquivo .env criado" -ForegroundColor Green
}

# 3. Aplicar migrações
Write-Host "🗄️  Aplicando migrações..." -ForegroundColor Blue
python manage.py makemigrations
python manage.py migrate
Write-Host "✅ Migrações aplicadas" -ForegroundColor Green

# 4. Criar superusuário
Write-Host "👤 Verificando superusuário..." -ForegroundColor Blue
python create_superuser.py
Write-Host "✅ Superusuário verificado" -ForegroundColor Green

# 5. Carregar dados de exemplo usando arquivo Python
Write-Host "📊 Carregando dados de exemplo..." -ForegroundColor Blue

# Criar script temporário para carregar dados
@"
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from produtos.models import Categoria, Produto
from clientes.models import Cliente
from decimal import Decimal

print("Carregando categorias...")
categorias_data = [
    {'nome': 'Alimentação', 'descricao': 'Produtos alimentícios'},
    {'nome': 'Bebidas', 'descricao': 'Bebidas em geral'},
    {'nome': 'Limpeza', 'descricao': 'Produtos de limpeza'},
    {'nome': 'Higiene', 'descricao': 'Produtos de higiene pessoal'},
    {'nome': 'Eletrônicos', 'descricao': 'Produtos eletrônicos'},
]

for cat_data in categorias_data:
    categoria, created = Categoria.objects.get_or_create(
        nome=cat_data['nome'],
        defaults=cat_data
    )
    if created:
        print(f"✅ Categoria criada: {categoria.nome}")

print("Carregando produtos...")
produtos_data = [
    {
        'codigo': 'PROD001',
        'nome': 'Arroz Branco 5kg',
        'categoria': 'Alimentação',
        'preco_custo': Decimal('8.50'),
        'preco_venda': Decimal('12.90'),
        'estoque_atual': 50,
        'estoque_minimo': 10,
        'descricao': 'Arroz branco tipo 1, pacote de 5kg'
    },
    {
        'codigo': 'PROD002', 
        'nome': 'Feijão Carioca 1kg',
        'categoria': 'Alimentação',
        'preco_custo': Decimal('4.20'),
        'preco_venda': Decimal('6.50'),
        'estoque_atual': 30,
        'estoque_minimo': 5,
        'descricao': 'Feijão carioca tipo 1, pacote de 1kg'
    },
    {
        'codigo': 'PROD003',
        'nome': 'Refrigerante Cola 2L',
        'categoria': 'Bebidas',
        'preco_custo': Decimal('3.80'),
        'preco_venda': Decimal('5.90'),
        'estoque_atual': 25,
        'estoque_minimo': 8,
        'descricao': 'Refrigerante sabor cola, garrafa 2 litros'
    },
    {
        'codigo': 'PROD004',
        'nome': 'Detergente Neutro 500ml',
        'categoria': 'Limpeza',
        'preco_custo': Decimal('1.50'),
        'preco_venda': Decimal('2.90'),
        'estoque_atual': 40,
        'estoque_minimo': 15,
        'descricao': 'Detergente neutro para louças, 500ml'
    },
    {
        'codigo': 'PROD005',
        'nome': 'Sabonete Antibacteriano',
        'categoria': 'Higiene',
        'preco_custo': Decimal('1.20'),
        'preco_venda': Decimal('2.50'),
        'estoque_atual': 60,
        'estoque_minimo': 20,
        'descricao': 'Sabonete antibacteriano 90g'
    },
    {
        'codigo': 'PROD006',
        'nome': 'Açúcar Cristal 1kg',
        'categoria': 'Alimentação',
        'preco_custo': Decimal('2.80'),
        'preco_venda': Decimal('4.50'),
        'estoque_atual': 45,
        'estoque_minimo': 12,
        'descricao': 'Açúcar cristal especial, pacote de 1kg'
    },
    {
        'codigo': 'PROD007',
        'nome': 'Água Mineral 500ml',
        'categoria': 'Bebidas',
        'preco_custo': Decimal('0.80'),
        'preco_venda': Decimal('1.50'),
        'estoque_atual': 100,
        'estoque_minimo': 30,
        'descricao': 'Água mineral natural, garrafa 500ml'
    },
    {
        'codigo': 'PROD008',
        'nome': 'Papel Higiênico 12 Rolos',
        'categoria': 'Higiene',
        'preco_custo': Decimal('8.90'),
        'preco_venda': Decimal('14.90'),
        'estoque_atual': 35,
        'estoque_minimo': 10,
        'descricao': 'Papel higiênico folha dupla, pacote com 12 rolos'
    }
]

for prod_data in produtos_data:
    categoria = Categoria.objects.get(nome=prod_data['categoria'])
    produto, created = Produto.objects.get_or_create(
        codigo=prod_data['codigo'],
        defaults={
            'nome': prod_data['nome'],
            'categoria': categoria,
            'preco_custo': prod_data['preco_custo'],
            'preco_venda': prod_data['preco_venda'],
            'estoque_atual': prod_data['estoque_atual'],
            'estoque_minimo': prod_data['estoque_minimo'],
            'descricao': prod_data.get('descricao', '')
        }
    )
    if created:
        print(f"✅ Produto criado: {produto.nome}")

print("Carregando clientes...")
clientes_data = [
    {
        'nome': 'João Silva Santos',
        'tipo_pessoa': 'F',
        'cpf_cnpj': '12345678901',
        'email': 'joao.silva@email.com',
        'telefone': '(85) 99999-1234',
        'endereco': 'Rua das Flores, 123',
        'bairro': 'Centro',
        'cidade': 'Fortaleza',
        'uf': 'CE',
        'cep': '60000-000'
    },
    {
        'nome': 'Maria Santos Oliveira',
        'tipo_pessoa': 'F', 
        'cpf_cnpj': '98765432100',
        'email': 'maria.santos@email.com',
        'telefone': '(85) 88888-5678',
        'endereco': 'Av. Principal, 456',
        'bairro': 'Eusébio',
        'cidade': 'Eusébio',
        'uf': 'CE',
        'cep': '61760-000'
    },
    {
        'nome': 'Empresa XYZ Comércio Ltda',
        'tipo_pessoa': 'J',
        'cpf_cnpj': '12345678000199',
        'email': 'contato@empresaxyz.com.br',
        'telefone': '(85) 3333-4444',
        'endereco': 'Rua Comercial, 789',
        'bairro': 'Aldeota',
        'cidade': 'Fortaleza',
        'uf': 'CE',
        'cep': '60150-000'
    },
    {
        'nome': 'Carlos Pereira Lima',
        'tipo_pessoa': 'F',
        'cpf_cnpj': '11122233344',
        'email': 'carlos.lima@email.com',
        'telefone': '(85) 77777-9999',
        'endereco': 'Rua do Comércio, 321',
        'bairro': 'Messejana',
        'cidade': 'Fortaleza',
        'uf': 'CE',
        'cep': '60840-000'
    },
    {
        'nome': 'Ana Paula Costa',
        'tipo_pessoa': 'F',
        'cpf_cnpj': '55566677788',
        'email': 'ana.costa@email.com',
        'telefone': '(85) 66666-1111',
        'endereco': 'Av. Washington Soares, 1000',
        'bairro': 'Edson Queiroz',
        'cidade': 'Fortaleza',
        'uf': 'CE',
        'cep': '60811-000'
    }
]

for cli_data in clientes_data:
    cliente, created = Cliente.objects.get_or_create(
        cpf_cnpj=cli_data['cpf_cnpj'],
        defaults=cli_data
    )
    if created:
        print(f"✅ Cliente criado: {cliente.nome}")

print("✅ Dados de exemplo carregados com sucesso!")
"@ | Out-File -FilePath "load_sample_data.py" -Encoding UTF8

# Executar o script de dados
python load_sample_data.py

# Remover o script temporário
Remove-Item "load_sample_data.py"

Write-Host "✅ Dados de exemplo carregados" -ForegroundColor Green

# 6. Coletar arquivos estáticos
Write-Host "📁 Coletando arquivos estáticos..." -ForegroundColor Blue
python manage.py collectstatic --noinput
Write-Host "✅ Arquivos estáticos coletados" -ForegroundColor Green

# 7. Verificar sistema
Write-Host "🔍 Verificando sistema..." -ForegroundColor Blue
python manage.py check
Write-Host "✅ Sistema verificado" -ForegroundColor Green

# 8. Informações finais
Write-Host ""
Write-Host "🎉 === SISTEMA PDV CONFIGURADO COM SUCESSO! ===" -ForegroundColor Green
Write-Host ""
Write-Host "📋 INFORMAÇÕES DE ACESSO:" -ForegroundColor Blue
Write-Host "🌐 URL Principal: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "👤 Usuário Admin: admin" -ForegroundColor Yellow
Write-Host "🔑 Senha Admin: admin123" -ForegroundColor Yellow
Write-Host ""
Write-Host "📱 PRINCIPAIS FUNCIONALIDADES:" -ForegroundColor Blue
Write-Host "   🏠 Dashboard: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "   💰 PDV (Vendas): http://127.0.0.1:8000/vendas/pdv/" -ForegroundColor Cyan
Write-Host "   📦 Produtos: http://127.0.0.1:8000/produtos/" -ForegroundColor Cyan
Write-Host "   👥 Clientes: http://127.0.0.1:8000/clientes/" -ForegroundColor Cyan
Write-Host "   📊 Relatórios: http://127.0.0.1:8000/relatorios/" -ForegroundColor Cyan
Write-Host "   ⚙️  Admin Django: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
Write-Host ""
Write-Host "🛠️  DADOS CARREGADOS:" -ForegroundColor Blue
Write-Host "   📂 5 Categorias de produtos" -ForegroundColor White
Write-Host "   📦 8 Produtos de exemplo" -ForegroundColor White
Write-Host "   👤 5 Clientes de exemplo" -ForegroundColor White
Write-Host ""
Write-Host "⌨️  ATALHOS DO PDV:" -ForegroundColor Blue
Write-Host "   F2 - Focar no campo de busca" -ForegroundColor White
Write-Host "   F12 - Finalizar venda" -ForegroundColor White
Write-Host ""

# 9. Opção de iniciar servidor
$resposta = Read-Host "🚀 Deseja iniciar o servidor agora? (s/n)"

if ($resposta -eq "s" -or $resposta -eq "S") {
    Write-Host ""
    Write-Host "🚀 Iniciando servidor Django..." -ForegroundColor Green
    Write-Host "   Pressione Ctrl+C para parar o servidor" -ForegroundColor Blue
    Write-Host ""
    python manage.py runserver
} else {
    Write-Host ""
    Write-Host "💡 Para iniciar o servidor manualmente, execute:" -ForegroundColor Blue
    Write-Host "   python manage.py runserver" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host "✨ Obrigado por usar o Sistema PDV!" -ForegroundColor Green