from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Articles

@register(Articles)
class ProductIndex(AlgoliaIndex):
    # should_index = 'is_public'
    fields=[
        'pk',
        'title',
        'body',
        'path',
        'endpoint',
        
    ]
    settings={
        'searchableAttributes':['title', 'content'],
        'attributesForFaceting':['user', 'public']
    }
    tags='get_tags_list'

