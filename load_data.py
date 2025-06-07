# load_data.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from produtos.models import Categoria, Produto
from clientes.models import Cliente
from decimal import Decimal

print("🔄 Carregando dados de exemplo no Sistema PDV...")

# Categorias
print("📂 Criando categorias...")
categorias = [
    {'nome': 'Alimentação', 'descricao': 'Produtos alimentícios'},
    {'nome': 'Bebidas', 'descricao': 'Bebidas em geral'},
    {'nome': 'Limpeza', 'descricao': 'Produtos de limpeza'},
    {'nome': 'Higiene', 'descricao': 'Produtos de higiene pessoal'},
    {'nome': 'Eletrônicos', 'descricao': 'Produtos eletrônicos'},
]

cat_criadas = 0
for cat in categorias:
    categoria, created = Categoria.objects.get_or_create(
        nome=cat['nome'], defaults=cat
    )
    if created:
        print(f"  ✅ Categoria criada: {categoria.nome}")
        cat_criadas += 1
    else:
        print(f"  ℹ️  Categoria já existe: {categoria.nome}")

print(f"📂 {cat_criadas} categorias criadas")

# Produtos
print("📦 Criando produtos...")
produtos = [
    {
        'codigo': 'PROD001', 'nome': 'Arroz Branco 5kg', 'categoria': 'Alimentação',
        'preco_custo': Decimal('8.50'), 'preco_venda': Decimal('12.90'),
        'estoque_atual': 50, 'estoque_minimo': 10,
        'descricao': 'Arroz branco tipo 1, pacote de 5kg'
    },
    {
        'codigo': 'PROD002', 'nome': 'Feijão Carioca 1kg', 'categoria': 'Alimentação',
        'preco_custo': Decimal('4.20'), 'preco_venda': Decimal('6.50'),
        'estoque_atual': 30, 'estoque_minimo': 5,
        'descricao': 'Feijão carioca tipo 1, pacote de 1kg'
    },
    {
        'codigo': 'PROD003', 'nome': 'Refrigerante Cola 2L', 'categoria': 'Bebidas',
        'preco_custo': Decimal('3.80'), 'preco_venda': Decimal('5.90'),
        'estoque_atual': 25, 'estoque_minimo': 8,
        'descricao': 'Refrigerante sabor cola, garrafa 2 litros'
    },
    {
        'codigo': 'PROD004', 'nome': 'Detergente Neutro 500ml', 'categoria': 'Limpeza',
        'preco_custo': Decimal('1.50'), 'preco_venda': Decimal('2.90'),
        'estoque_atual': 40, 'estoque_minimo': 15,
        'descricao': 'Detergente neutro para louças'
    },
    {
        'codigo': 'PROD005', 'nome': 'Sabonete Antibacteriano', 'categoria': 'Higiene',
        'preco_custo': Decimal('1.20'), 'preco_venda': Decimal('2.50'),
        'estoque_atual': 60, 'estoque_minimo': 20,
        'descricao': 'Sabonete antibacteriano 90g'
    },
    {
        'codigo': 'PROD006', 'nome': 'Açúcar Cristal 1kg', 'categoria': 'Alimentação',
        'preco_custo': Decimal('2.80'), 'preco_venda': Decimal('4.50'),
        'estoque_atual': 45, 'estoque_minimo': 12,
        'descricao': 'Açúcar cristal especial'
    },
    {
        'codigo': 'PROD007', 'nome': 'Água Mineral 500ml', 'categoria': 'Bebidas',
        'preco_custo': Decimal('0.80'), 'preco_venda': Decimal('1.50'),
        'estoque_atual': 100, 'estoque_minimo': 30,
        'descricao': 'Água mineral natural'
    },
    {
        'codigo': 'PROD008', 'nome': 'Papel Higiênico 12 Rolos', 'categoria': 'Higiene',
        'preco_custo': Decimal('8.90'), 'preco_venda': Decimal('14.90'),
        'estoque_atual': 35, 'estoque_minimo': 10,
        'descricao': 'Papel higiênico folha dupla'
    }
]

prod_criados = 0
for prod in produtos:
    try:
        categoria = Categoria.objects.get(nome=prod['categoria'])
        produto, created = Produto.objects.get_or_create(
            codigo=prod['codigo'],
            defaults={
                'nome': prod['nome'],
                'categoria': categoria,
                'preco_custo': prod['preco_custo'],
                'preco_venda': prod['preco_venda'],
                'estoque_atual': prod['estoque_atual'],
                'estoque_minimo': prod['estoque_minimo'],
                'descricao': prod.get('descricao', '')
            }
        )
        if created:
            print(f"  ✅ Produto criado: {produto.nome}")
            prod_criados += 1
        else:
            print(f"  ℹ️  Produto já existe: {produto.nome}")
    except Exception as e:
        print(f"  ❌ Erro ao criar produto {prod['codigo']}: {e}")

print(f"📦 {prod_criados} produtos criados")

# Clientes
print("👥 Criando clientes...")
clientes = [
    {
        'nome': 'João Silva Santos', 'tipo_pessoa': 'F', 'cpf_cnpj': '12345678901',
        'email': 'joao.silva@email.com', 'telefone': '(85) 99999-1234',
        'endereco': 'Rua das Flores, 123', 'bairro': 'Centro',
        'cidade': 'Fortaleza', 'uf': 'CE', 'cep': '60000-000'
    },
    {
        'nome': 'Maria Santos Oliveira', 'tipo_pessoa': 'F', 'cpf_cnpj': '98765432100',
        'email': 'maria.santos@email.com', 'telefone': '(85) 88888-5678',
        'endereco': 'Av. Principal, 456', 'bairro': 'Eusébio',
        'cidade': 'Eusébio', 'uf': 'CE', 'cep': '61760-000'
    },
    {
        'nome': 'Empresa XYZ Comércio Ltda', 'tipo_pessoa': 'J', 'cpf_cnpj': '12345678000199',
        'email': 'contato@empresaxyz.com.br', 'telefone': '(85) 3333-4444',
        'endereco': 'Rua Comercial, 789', 'bairro': 'Aldeota',
        'cidade': 'Fortaleza', 'uf': 'CE', 'cep': '60150-000'
    },
    {
        'nome': 'Carlos Pereira Lima', 'tipo_pessoa': 'F', 'cpf_cnpj': '11122233344',
        'email': 'carlos.lima@email.com', 'telefone': '(85) 77777-9999',
        'endereco': 'Rua do Comércio, 321', 'bairro': 'Messejana',
        'cidade': 'Fortaleza', 'uf': 'CE', 'cep': '60840-000'
    },
    {
        'nome': 'Ana Paula Costa', 'tipo_pessoa': 'F', 'cpf_cnpj': '55566677788',
        'email': 'ana.costa@email.com', 'telefone': '(85) 66666-1111',
        'endereco': 'Av. Washington Soares, 1000', 'bairro': 'Edson Queiroz',
        'cidade': 'Fortaleza', 'uf': 'CE', 'cep': '60811-000'
    }
]

cli_criados = 0
for cli in clientes:
    cliente, created = Cliente.objects.get_or_create(
        cpf_cnpj=cli['cpf_cnpj'], defaults=cli
    )
    if created:
        print(f"  ✅ Cliente criado: {cliente.nome}")
        cli_criados += 1
    else:
        print(f"  ℹ️  Cliente já existe: {cliente.nome}")

print(f"👥 {cli_criados} clientes criados")

print()
print("🎉 === DADOS DE EXEMPLO CARREGADOS COM SUCESSO! ===")
print()
print(f"📊 RESUMO FINAL:")
print(f"   📂 {Categoria.objects.count()} Categorias")
print(f"   📦 {Produto.objects.count()} Produtos")
print(f"   👤 {Cliente.objects.count()} Clientes")
print()
print("🚀 SISTEMA PRONTO PARA USO!")
print()
print("📱 ACESSE AS FUNCIONALIDADES:")
print("   🏠 Dashboard: http://127.0.0.1:8000/")
print("   💰 PDV: http://127.0.0.1:8000/vendas/pdv/")
print("   📦 Produtos: http://127.0.0.1:8000/produtos/")
print("   👥 Clientes: http://127.0.0.1:8000/clientes/")
print("   ⚙️  Admin: http://127.0.0.1:8000/admin/")
print()
print("👤 LOGIN ADMIN: admin / admin123")