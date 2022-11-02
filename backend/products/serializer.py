from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Products
from . import validators
from api.serializers import  UserPublicSerializer


class ProductsInlineSerializer(serializers.Serializer):
    url= serializers.HyperlinkedIdentityField(
        view_name= 'product-detail',
        lookup_field='pk',
        read_only= True
        )
    title = serializers.CharField(read_only=True)

class ProductsSerializers(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user',read_only=True)
    # related_products = ProductsInlineSerializer(source = 'user.products_set.all', read_only=True, many=True)
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    # discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url= serializers.HyperlinkedIdentityField(
        view_name= 'product-detail',
        lookup_field='pk'
        )
    # email = serializers.EmailField(write_only=True)
    title= serializers.CharField(validators=[validators.unique_product_title,
    validators.unique_product_title])
    body= serializers.CharField(source='content')
    class Meta:
        model= Products
        fields=[
            'owner',
            'url',
            'edit_url',
            # 'email',
            'pk',
            'title',
            'body', 
            'price',
            'sale_price',
            'public',
            'path'
            # 'get_discount_price',
            # 'discount',
            # 'my_user_data',
            # 'related_products'
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
        return Products.objects.create(**validated_data)
        obj= super().create(validated_data)
        # print(email, obj)
        return obj 

    def get_edit_url(self, obj):
        return f"api/product/{obj.pk}/"
        request= self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)

    def get_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        # print(obj.id)
        return obj.get_discount_price()
        #obj.user->user.name 
        #  # try:
        #     return ()
        # except: