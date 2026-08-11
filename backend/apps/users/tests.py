from django.test import TestCase
from .models import User
from rest_framework.test import APITestCase
from django.urls import reverse

class UserModelTest(TestCase):
    def test_create_user_with_email_successful(self):
        user = User.objects.create_user(
            email = "test@example.com",
            password = "testpass123")

        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email = "",
                password = "testpass123"
            )

    def test_create_superuser_successful(self):
        superuser = User.objects.create_superuser(
            email = "test1@example.com",
            password = "testpass1234")

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class RegisterAPITest(APITestCase):
    """
    Testes do endpoint POST /api/auth/register/ (Fatia 1 da Tarefa 5).

    Convenção de nome: test_<condição>_<resultado esperado>. Quando um teste
    fica vermelho no CI, muitas vezes o nome é a única coisa que se lê.

    Cada método roda em sua própria transação, com rollback ao final — nada
    que um teste cria sobrevive para o próximo, então repetir o mesmo email
    entre testes diferentes é seguro.
    """

    def setUp(self):
        self.url = reverse('register')

    def test_valid_registration_returns_201(self):
        """Caminho feliz: email e senha válidos criam a conta e devolvem 201."""
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_missing_password_field_returns_400(self):
        """Senha é obrigatória: sem o campo, o serializer rejeita com 400."""
        response = self.client.post(self.url, {
            'email': 'test@example.com'
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_uppercase_email_is_normalized_to_lowercase(self):
        """
        Protege a LowerEmailField: o email chega em MAIÚSCULO e tem que ser
        gravado minúsculo. O User.objects.get() abaixo é a asserção de fato —
        ele levanta DoesNotExist se a normalização não tiver acontecido.
        """
        response = self.client.post(self.url, {
            'email': 'TEST@EXAMPLE.COM',
            'password': 'testpass123',
        }, format='json')
        User.objects.get(email='test@example.com')
        self.assertEqual(response.status_code, 201)

    def test_duplicate_email_same_case_returns_400(self):
        """
        Duplicata trivial: mesmo email, mesma caixa. Protege o UniqueValidator
        reanexado no campo declarado — sem ele a constraint do banco estoura
        IntegrityError e o cliente recebe 500 em vez de 400.
        """
        User.objects.create_user(
            email = "test@example.com",
            password = "testpass123")
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_duplicate_email_different_case_returns_400(self):
        """
        Regressão do bug corrigido em 2026-08-10.

        Conta criada em minúsculo, nova tentativa em MAIÚSCULO. Antes da
        LowerEmailField, o UniqueValidator fazia busca `exact`, não encontrava
        a duplicata e aprovava a entrada — só então o save() normalizava e a
        UniqueConstraint(Lower('email')) estourava IntegrityError → HTTP 500.

        É o único teste deste arquivo que falharia com o código de ontem: o de
        mesma caixa, acima, passava mesmo com o bug vivo.
        """
        User.objects.create_user(
            email = "maria@example.com",
            password = "testpass123")
        response = self.client.post(self.url, {
            'email': 'MARIA@EXAMPLE.COM',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)

    def test_response_does_not_contain_password(self):
        """
        Protege o write_only=True do campo password.

        Sem ele o corpo do 201 devolve o hash da senha. O risco é concreto:
        `extra_kwargs` é ignorado silenciosamente em campo declarado, então dá
        para achar que o write_only está ligado quando não está.
        """
        response = self.client.post(self.url, {
            'email': 'joao@example.com',
            'password': 'testpass123',
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.data)

    def test_short_password_returns_400(self):
        """
        Protege o MinimumLengthValidator (min_length=8, requisito da US-02).

        O email é `usuario@` de propósito: com `test@example.com`, o validador
        de semelhança dispararia junto e o 400 viria por outro motivo — o teste
        ficaria verde mesmo se o min_length fosse removido do settings.
        """
        response = self.client.post(self.url, {
            'email': 'usuario@example.com',
            'password': 'test',
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_password_similar_to_email_returns_400(self):
        """
        Protege o UserAttributeSimilarityValidator — o único dos quatro que
        exige um objeto `user`. Se alguém remover o `user=` da chamada a
        validate_password(), ele volta a ser pulado em silêncio, sem erro nem
        warning, e só este teste percebe.
        """
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'test@example.com',
        }, format='json')
        self.assertIn('password', response.data)
        self.assertEqual(response.status_code, 400)

    def test_get_on_route_returns_405(self):
        """
        Garante que a rota só aceita POST. Com um ModelViewSet no lugar do
        CreateAPIView, este GET devolveria a lista de todos os usuários.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_password_is_not_stored_in_plain_text(self):
        """
        Protege o create() sobrescrito, que chama create_user() em vez do
        objects.create() padrão do ModelSerializer — este último gravaria a
        senha em texto puro e devolveria 201 sem reclamar.

        As duas asserções são necessárias: a primeira sozinha passaria se o
        código gravasse qualquer lixo no campo; a segunda confirma que o hash
        guardado é o da senha certa.
        """
        response = self.client.post(self.url, {
            'email': 'test@example.com',
            'password': 'testpass123',
        }, format='json')
        user = User.objects.get(email='test@example.com')
        self.assertNotEqual(user.password, 'testpass123')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(response.status_code, 201)
