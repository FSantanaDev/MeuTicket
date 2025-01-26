#################Models.py ###################





from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

class Area(models.Model):
    nomearea = models.CharField(max_length=100)

    def __str__(self):
        return self.nomearea




class Perfil(models.Model):
    tipo = models.CharField(max_length=50, choices=[('operador', 'Operador'), ('suporte', 'Suporte')])

    def __str__(self):
        return self.tipo



class Servico(models.Model):
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao


class Urgencia(models.Model):
    URGENCIA_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    nivel = models.CharField(max_length=7, choices=URGENCIA_CHOICES)

    def __str__(self):
        return self.get_nivel_display()


   
    
    
    
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário deve ter um email")
        usuario = self.model(email=self.normalize_email(email), **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')#
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)





class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Email como identificador único
    nome = models.CharField(max_length=100, unique=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    perfil = models.ForeignKey('Perfil', on_delete=models.SET_NULL, null=True, blank=True)
    area = models.ForeignKey('Area', on_delete=models.SET_NULL, null=True, blank=True)
    data_criacao = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'  # Define o email como campo de autenticação
    REQUIRED_FIELDS = ['nome', 'cpf']  # Campos obrigatórios ao criar superuser

    def __str__(self):
        return self.email



    
class Demanda(models.Model):
    # Define uma classe chamada Demanda que herda de models.Model, 
    # o que significa que esta classe representa uma tabela no banco de dados.
    
    STATUS_CHOICES = [
        ('Aberto', 'Aberto'),
        ('Fechado', 'Fechado'),
    ]
    # Define uma lista de tuplas chamada STATUS_CHOICES que contém as opções de status 
    # que uma demanda pode ter. Cada tupla contém o valor que será armazenado no banco de dados 
    # e o valor que será exibido para o usuário.

    titulo = models.CharField(max_length=100)
    # Define um campo de texto chamado 'titulo' com um comprimento máximo de 100 caracteres.

    descricao = models.TextField()
    # Define um campo de texto longo chamado 'descricao' para armazenar a descrição da demanda.

    imagem = models.ImageField(upload_to='demandas/', null=True, blank=True)
    # Define um campo para upload de imagem chamado 'imagem'. 
    # As imagens serão salvas no diretório 'demandas/' dentro do diretório de mídia.
    # O campo pode ser nulo (null=True) e não é obrigatório (blank=True).

    area = models.ForeignKey('Area', on_delete=models.CASCADE)
    # Define um campo de chave estrangeira chamado 'area' que se relaciona com o modelo 'Area'.
    # Quando uma 'Area' é deletada, todas as demandas relacionadas a ela também serão deletadas (CASCADE).

    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='Aberto')
    # Define um campo de texto chamado 'status' que pode ter no máximo 7 caracteres.
    # O campo usa as opções definidas em STATUS_CHOICES e tem um valor padrão 'Aberto'.

    data_criacao = models.DateTimeField(auto_now_add=True)
    # Define um campo de data e hora chamado 'data_criacao'.
    # O campo é automaticamente preenchido com a data e hora atuais quando a demanda é criada (auto_now_add=True).

    operador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='demandas_abertas')
    # Define um campo de chave estrangeira chamado 'operador' que se relaciona com o modelo de usuário autenticado.
    # Quando o usuário é deletado, todas as demandas relacionadas a ele também serão deletadas (CASCADE).
    # O related_name='demandas_abertas' permite acessar todas as demandas abertas por um usuário específico.

    realizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='demandas_realizadas'
    )
    # Define um campo de chave estrangeira chamado 'realizador' que também se relaciona com o modelo de usuário autenticado.
    # Quando o usuário é deletado, o campo é definido como NULL (SET_NULL).
    # O campo pode ser nulo (null=True) e não é obrigatório (blank=True).
    # O related_name='demandas_realizadas' permite acessar todas as demandas realizadas por um usuário específico.

    realizadoem = models.DateTimeField(null=True, blank=True)
    # Define um campo de data e hora chamado 'realizadoem'.
    # O campo pode ser nulo (null=True) e não é obrigatório (blank=True).

    servico = models.ForeignKey('Servico', on_delete=models.CASCADE)
    # Define um campo de chave estrangeira chamado 'servico' que se relaciona com o modelo 'Servico'.
    # Quando um 'Servico' é deletado, todas as demandas relacionadas a ele também serão deletadas (CASCADE).

    urgencia = models.ForeignKey('Urgencia', on_delete=models.CASCADE)
    # Define um campo de chave estrangeira chamado 'urgencia' que se relaciona com o modelo 'Urgencia'.
    # Quando uma 'Urgencia' é deletada, todas as demandas relacionadas a ela também serão deletadas (CASCADE).

    chave = models.CharField(max_length=20, unique=True, null=True, blank=True)
    # Define um campo de texto chamado 'chave' com um comprimento máximo de 20 caracteres.
    # O campo deve ser único (unique


class Mensagem(models.Model):
    demanda = models.ForeignKey(Demanda, related_name='mensagens', on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.autor.get_full_name} em {self.data_envio}"










# Create your models here.
