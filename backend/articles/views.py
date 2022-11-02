from django.shortcuts import render
from .models import Articles
from rest_framework import generics, mixins, authentication, permissions
from .serializers import ArticleSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import Http404
from django.shortcuts import get_object_or_404
from api.mixins import  (UserQuerySetMixin)

class ArticleListView(generics.ListAPIView):
    queryset = Articles.objects.public()
    serializer_class = ArticleSerializers


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Articles.objects.public()
    serializer_class =ArticleSerializers



class ArticlesListCreateAPIView(UserQuerySetMixin
,generics.ListCreateAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializers
    # user_field = 'owner' =>this will throw an error
    permission_classes =[permissions.IsAdminUser]
# permission_classes =[permissions.IsAdminUser, iStaffArticlesEditorPermissions] what permission you want to match first you should put first 

    def perfom_create(self, serializer):
        print(serializer.validated_data)
        title= serializer.validated_data.get('title')
        body= serializer.validated_data.get('body') or None 
        if body is None:
            body=title
        serializer.save(user=self.request.user, body=body)

    def get_queryset(self,*args, **kwargs):
       qs= super().get_queryset(*args, **kwargs)
       resquest = self.request
       user= resquest.user
    #    print(resquest.user) 
       return qs.filter(user=resquest.user)
        
articles_list_create_view = ArticlesListCreateAPIView.as_view()


class ArticleMixinView(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        UserQuerySetMixin,
                        generics.GenericAPIView):
    queryset= Articles.objects.all()
    serializer_class=ArticleSerializers
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk=kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
         
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

article_mixin_views = ArticleMixinView.as_view()

