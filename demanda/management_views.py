from django.http import HttpResponse
from django.core.management import call_command
from django.shortcuts import render

def run_migrations(request):
    try:
        # Executando as migrações do banco de dados
        call_command('migrate')
        return HttpResponse("Migrações executadas com sucesso!")
    except Exception as e:
        # Retornando erro caso aconteça
        return HttpResponse(f"Erro ao executar migrações: {e}")