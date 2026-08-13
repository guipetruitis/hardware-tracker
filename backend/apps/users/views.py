from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response 

class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Permite acesso público para registro de usuários, sem ela, o endpoint de registro exigiria autenticação, o que não é desejável para novos usuários que ainda não possuem credenciais.

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # Permite acesso público para login de usuários, sem ela, o endpoint de login exigiria autenticação, o que não é desejável para usuários que ainda não possuem credenciais.

    def post(self, request, *args, **kwargs):
        """
        Endpoint de login. Recebe email e senha
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        return Response(UserSerializer(user).data)
