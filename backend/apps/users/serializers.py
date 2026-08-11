from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password as DjangoValidatePassword
from django.core.exceptions import ValidationError as DjangoValidationError

class LowerEmailField(serializers.EmailField):
    """
    Classe personalizada para normalizar o campo de e-mail.
    """
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data = data.lower() 
         
        return data

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    ''' 
    UserSerializer é uma classe de serializador que lida com a serialização e desserialização de objetos da classe User. Ele define os campos que serão incluídos na representação JSON do objeto, bem como as validações necessárias para cada campo.
    '''

    class Meta:
        model = User
        fields = ['id', 'email']

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    '''
    RegisterSerializer é uma classe de serializador que lida com a criação de usuários 
    '''

    email = LowerEmailField(
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(write_only=True, max_length=128, required=True, style={'input_type': 'password'})

    def validate(self, attrs): 
        """
        Valida a senha aqui,e nao em um validador do campo, porque o UserAttributeSimilarityValidator precisa de um objeto 'User' para funcionar, e assim comparar a senha com o email do usuario.
        """
        user = User(email=attrs['email'])

        try:
            DjangoValidatePassword(attrs['password'], user=user)
        
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': e.messages})
                
        return attrs

    def create(self, validated_data):
        
        user = User.objects.create_user(**validated_data)
    
        return user


    class Meta:
        model = User
        fields = ['id', 'email', 'password']


