from rest_framework import serializers

from api.serializers import UserPublicSerializer
from .models import Articles
from . import validators

class ArticleSerializers (serializers.ModelSerializer):
    author = UserPublicSerializer(source='user', read_only=True)
    title= serializers.CharField(validators=[validators.unique_article_title,
    validators.unique_article_title])

    body= serializers.CharField(source='content')
    class Meta:
        model = Articles
        fields = [
            'pk',
            'author',
            'title',
            'body',
            'path',
            'endpoint',
        ]




    # def validate_title(self, value):
    #     qs= Products.objects.filter(title__exact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name.")
    #     return value

    def get_my_user_data(self, obj):
        return{
            "user":obj.user.username
        }

    def create(self, validated_data):
        # email= validated_data.pop('email')
        return Articles.objects.create(**validated_data)
        obj= super().create(validated_data)
        # print(email, obj)
        return obj 