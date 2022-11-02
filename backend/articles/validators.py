from rest_framework import serializers
from .models import Articles
from rest_framework.validators import UniqueValidator


def validate_title_no_hello(value):
    if"hello" in value.lower():
        raise serializers.ValidationError(f"{value} is not allowed")
    return value


unique_article_title= UniqueValidator(queryset=Articles.objects.all(),
lookup='iexact')