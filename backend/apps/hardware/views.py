from rest_framework import viewsets
from .models import Category, Store, Hardware
from .serializers import CategorySerializer, StoreSerializer, HardwareSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet ):

    ''' A viewset de Category é responsável por lidar com as requisições HTTP relacionadas à classe Category. Ela herda de ModelViewSet, que fornece implementações padrão para operações CRUD (Create, Read, Update, Delete) no caso é somente leitura em objetos do modelo. A viewset define o queryset e o serializer_class que serão usados para processar as requisições.

    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class StoreViewSet(viewsets.ReadOnlyModelViewSet ):

    queryset = Store.objects.filter(is_active=True)
    serializer_class = StoreSerializer

class HardwareViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Hardware.objects.filter(deleted_at__isnull=True)
    serializer_class = HardwareSerializer