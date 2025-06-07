import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser criado com sucesso!')
    print('Usuario: admin')
    print('Senha: admin123')
    print('Email: admin@example.com')
else:
    print('Superuser ja existe!')
