from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    '''
    Classe personalizada para gerenciar a criação de usuários.
    esta classe herda de BaseUserManager e fornece métodos para criar usuários e superusuários.
    '''
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Usuário deve ter um endereço de e-mail válido')
        
        email = self.normalize_email(email) # Normaliza o e-mail para garantir consistência (por exemplo, convertendo para minúsculas)
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

    # Define o método __str__ para retornar o e-mail do usuário como representação em string da instância do modelo User
    def __str__(self):
        return self.email   