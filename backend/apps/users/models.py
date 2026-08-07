from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.functions import Lower

class UserManager(BaseUserManager):
    '''
    Classe personalizada para gerenciar a criação de usuários.
    esta classe herda de BaseUserManager e fornece métodos para criar usuários e superusuários.
    '''
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Usuário deve ter um endereço de e-mail válido')
        
        email = self.normalize_email(email) 
        user = self.model(email=email, **extra_fields) # Cria uma instância do modelo User com o e-mail fornecido e quaisquer outros campos adicionais passados como kwargs
        user.set_password(password) 
        user.save(using=self._db) 

        return user # Retorna a instância do usuário criado

    def create_superuser(self, email, password=None, **extra_fields): #**
        extra_fields.setdefault('is_staff', True) # Define o campo is_staff como True, indicando que o usuário é um membro da equipe administrativa
        extra_fields.setdefault('is_superuser', True) # Define o campo is_superuser como True, indicando que o usuário tem permissões de superusuário

        if extra_fields.get('is_staff') is not True: # Verifica se o campo is_staff é True
            raise ValueError('Superusuário deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True: # Verifica se o campo is_superuser é True
            raise ValueError('Superusuário deve ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields) # Chama o método create_user para criar o superusuário com os parâmetros fornecidos

    
    def get_by_natural_key(self, username):
        # Normaliza a ENTRADA; a comparação segue exata para usar o índice
        return super().get_by_natural_key(username.lower().strip())
        
class User(AbstractBaseUser, PermissionsMixin):
    '''
    Classe personalizada para representar um usuário no sistema.
    Esta classe herda de AbstractBaseUser e PermissionsMixin, permitindo a personalização do modelo de usuário padrão do Django.
    '''

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs): 
        # lower() na string toda: normalize_email() do Django só baixa o domínio (RFC 5321),
        # e neste projeto email é identidade case-insensitive  
        self.email = self.email.lower().strip()     # limpa e padroniza a STRING
        super().save(*args, **kwargs)               # Chama o método save da classe pai para realizar a operação de salvamento no banco de dados

    class Meta:
        constraints = [
            models.UniqueConstraint(Lower('email'), name='unique_user_email_lowercase')                           
        ]   

    # Define o método __str__ para retornar o e-mail do usuário como representação em string da instância do modelo User
    def __str__(self):
        return self.email   