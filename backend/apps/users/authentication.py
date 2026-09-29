from rest_framework_simplejwt.authentication import JWTAuthentication
from .constants import ACCESS_COOKIE_NAME, REFRESH_COOKIE_NAME

class CookieJWTAuthentication(JWTAuthentication):
    """
    Autentica pelo JWT guardado no cookie de access, em vez do header
    Authorization.

    Herda de JWTAuthentication por dois motivos. O primeiro é reaproveitar o
    miolo: get_validated_token() e get_user() não sabem de onde a credencial
    veio e não precisam saber, então a única coisa que esta classe escreve é
    o transporte. O segundo é o authenticate_header(): quando esta classe
    entrar à frente da JWTAuthentication em DEFAULT_AUTHENTICATION_CLASSES,
    é a ela que o DRF vai perguntar qual WWW-Authenticate mandar num 401 — e
    uma classe que devolvesse None ali faria o DRF rebaixar todo 401 para
    403, em silêncio.

    PENDENTE (P-21): falta aplicar CSRF quando a credencial vem do cookie. O
    DRF envolve toda APIView em csrf_exempt, então o CsrfViewMiddleware não
    roda. Com o token no header isso é correto, porque header não vai
    automático; com ele no cookie, o navegador anexa sozinho e o app ganha
    autoridade ambiente — hoje defendida só pelo SameSite=Lax.

    PENDENTE: esta classe ainda não está em DEFAULT_AUTHENTICATION_CLASSES.
    Até isso acontecer, nenhuma requisição real do projeto passa por aqui.
    """
    def authenticate(self, request):
        """
        Devolve (usuário, token validado) quando o cookie traz um token
        válido, e None quando não há cookie.

        O None não é escolha de estilo: é o contrato do DRF para "não é
        comigo, tenta a próxima classe da lista". Levantar exceção aqui
        impediria a JWTAuthentication seguinte de rodar, e quem autentica por
        header — o bot de ofertas do Telegram — pararia de entrar.

        Cookie presente mas com token inválido ou expirado não cai no None:
        get_validated_token() levanta InvalidToken sozinho, que é o terceiro
        ramo do contrato.
        """
        access_token = request.COOKIES.get(ACCESS_COOKIE_NAME)  # Obtém o token de acesso do cookie da requisição
        if not access_token:
            return None

        validated_token = self.get_validated_token(access_token)

        return self.get_user(validated_token), validated_token
        