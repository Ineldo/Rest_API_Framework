from rest_framework import  generics, mixins, authentication, permissions
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Products
from .serializer  import ProductsSerializers
from api.mixins import  (StaffEditorPermissionsMixin,UserQuerySetMixin)


class ProductListCreateAPIView(StaffEditorPermissionsMixin,UserQuerySetMixin
,generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializers
    # user_field = 'owner' =>this will throw an error
    permission_classes =[permissions.IsAdminUser]
# permission_classes =[permissions.IsAdminUser, iStaffProductEditorPermissions] what permission you want to match first you should put first 

    def perfom_create(self, serializer):
        print(serializer.validated_data)
        email= serializer.validated_data.pop('email')
        print(email)
        title= serializer.validated_data.get('title')
        content= serializer.validated_data.get('content') or None 
        if content is None:
            content=title
        serializer.save(user=self.request.user, content=content)

    # def get_queryset(self,*args, **kwargs):
    #    qs= super().get_queryset(*args, **kwargs)
    #    resquest = self.request
    #    user= resquest.user
    # #    print(resquest.user) 
    #    return qs.filter(user=resquest.user)
        
product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(StaffEditorPermissionsMixin, UserQuerySetMixin,
    generics.RetrieveAPIView):
    queryset= Products.objects.all()
    serializer_class=ProductsSerializers

product_detail_view=ProductDetailAPIView.as_view()

class ProductDeleteAPIView(
    StaffEditorPermissionsMixin,UserQuerySetMixin,
    generics.DestroyAPIView):
    queryset= Products.objects.all()
    serializer_class=ProductsSerializers
    # permission_classes =[permissions.DjangoModelPermissions]

    lookup_field = 'pk'

    def perform_destroy(self, instace):
        #instace
        super().perform_destroy(instace)

product_delete_view = ProductDeleteAPIView.as_view()



class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset= Products.objects.all()
    serializer_class=ProductsSerializers
    lookup_field = 'pk'
    permission_classes =[permissions.DjangoModelPermissions]


    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content =instance.title
        

product_update_view = ProductUpdateAPIView.as_view()

class ProductMixinView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        UserQuerySetMixin,
                        generics.GenericAPIView):
    queryset= Products.objects.all()
    serializer_class=ProductsSerializers
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk=kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
         
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

product_mixin_views = ProductMixinView.as_view()


@api_view(['POST','GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            #detail view
            obj=get_object_or_404(Products, pk=pk)
            data= ProductsSerializers(obj, many=False).data
            return Response(data)
        #list view
        querySet= Products.objects.all()
        data=ProductsSerializers(querySet, many=True).data
        return Response(data)
    if method == "POST":
        #create an item
        serializer=ProductsSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
                # instance=serializer.save()
            title= serializer.validated_data.get('title')
            content= serializer.validated_data.get('content') or None 
            if content is None:
                content=title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid":"not so good data"}, status=400)
   

