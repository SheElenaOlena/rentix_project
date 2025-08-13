import os
import django
from django.core.management import call_command

# Укажи имя проекта — то, что указано в manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rentix_projects.settings')  # если проект называется rentix
django.setup()

with open('full_data.json', 'w', encoding='utf-8') as f:
    call_command('dumpdata', indent=2, stdout=f)
