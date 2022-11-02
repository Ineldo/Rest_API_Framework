from rest_framework import viewsets

from .serializer import ProductsSerializers
from .models import Products


class ProductViewSet (viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializers
    lookup_field = 'pk'