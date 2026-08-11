from .serializers import RegisterSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Permite acesso público para registro de usuários, sem ela, o endpoint de registro exigiria autenticação, o que não é desejável para novos usuários que ainda não possuem credenciais.


# Faltando Login e User