from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response 
from django.conf import settings
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.signals import user_logged_in
from .constants import ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME
class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Permite acesso público para registro de usuários, sem ela, o endpoint de registro exigiria autenticação, o que não é desejável para novos usuários que ainda não possuem credenciais.

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]  # Permite acesso público para login de usuários, sem ela, o endpoint de login exigiria autenticação, o que não é desejável para usuários que ainda não possuem credenciais.

    def post(self, request, *args, **kwargs):
        """
        Endpoint de login.

        Recebe email e senha. Devolve o usuário no corpo e o par de tokens em DOIS cookies HttpOnly — nunca no JSON, que
        é o que mantém o token invisível para o JavaScript.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # O receiver update_last_login do Django já vem conectado a este sinal.
        # O request= não é usado por ele, mas é o que os receivers de auditoria
        # da P-05 vão querer (IP, user agent) sem precisar tocar nesta linha.
        user_logged_in.send(sender=user.__class__, request=request, user=user) # Envia um sinal de login, permitindo que outros componentes do sistema reajam ao evento de login, como registrar a atividade do user ou atualizar status de sessao
        
        refresh = RefreshToken.for_user(user) # Gera um token de atualizaçao para o usuario, permitindo que ele obtenha novos tokens de acesso sem precisar fazer login novamente, melhorando a experiencia do usuario e a segurança da aplicaçao
        access = refresh.access_token  # property: deriva um access novo do refresh

        response = Response(UserSerializer(user).data)

        # str() é obrigatório: estes são objetos Token, não strings.
        # max_age derivado do lifetime do token, nunca um número na mão —
        # total_seconds() devolve float, daí o int().
        response.set_cookie(
            ACCESS_COOKIE_NAME,
            str(access),
            max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite='Lax',
            path='/',
        )

        # Path derivado de reverse(): tira a credencial de 7 dias de ~99% do
        # tráfego. Atenção ao REFRESH_TOKEN_LIFETIME aqui — copiar o lifetime
        # do access mataria este cookie em 15min e nenhum teste perceberia.
        response.set_cookie(
            REFRESH_COOKIE_NAME,
            str(refresh),
            max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
            httponly=True,
            secure=settings.COOKIE_SECURE,
            samesite='Lax',
            path=reverse('refresh'),
        )

        return response

