from django.db.models import Count

from .models import *
from django.core.cache import cache

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]

class DataMixin:
     def get_user_context(self, **kwargs):
         context = kwargs
         cats =cache.get('cats')
         if not cats:
             cats = Category.objects.annotate(Count('women'))
             cache.set('cats', cats, 60)
         cats = Category.objects.all()
         context['menu'] = menu
         context['cats'] = cats
         if 'cat_selected' not in context:
                 context['cat_selected'] = 0
         return context
