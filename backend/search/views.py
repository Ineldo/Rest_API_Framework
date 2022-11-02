from rest_framework import generics

from products.models import Products
from rest_framework.response import Response
from products.serializer import ProductsSerializers
from . import client



class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        query= request.GET.get('q')
        public= str(request.GET.get('public')) != "0"
        tag= request.GET.get('tag') or None
        # print(user, tag, public, query)
        if not query:
            return Response('', status=404)
        results = client.perform_search(query, tags=[tag], user=user, public=public)
        return Response(results)

class SearchListOldView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class= ProductsSerializers

    def get_queryset(self, *args, **kwargs):
        qs= super().get_queryset(*args, **kwargs)
        q=self.request.GET.get('q')
        results = Products.objects.none()
        if q is not None:
            user= None
            if self.request.user.is_authenticated:
                user= self.request.user
            results=qs.search(q, user=user)
        return results