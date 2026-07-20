from rest_framework import serializers
from .models import Category, Store, Hardware


class CategorySerializer(serializers.ModelSerializer):
    
    ''' O serializer de Category é usado para serializar e desserializar objetos da classe Category. Ele define os campos que serão incluídos na representação JSON do objeto, bem como as validações necessárias para cada campo. '''

    class Meta: 
        model = Category
        fields = ['id', 'name', 'slug']

class StoreSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Store
        fields = ['id', 'name', 'slug', 'url', 'logo_url']

class HardwareSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Hardware
        fields = ['id', 'name', 'category', 'manufacturer', 'model', 'sku', 'specifications', 'image_url', 'description']        