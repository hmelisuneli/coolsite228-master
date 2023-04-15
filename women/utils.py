from django.db.models import Count

from .models import *
from django.core.cache import cache

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Запись", 'url_name': 'crud'},
]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
         # cats =cache.get('cats')
        cats=Category.objects.annotate(Count('women'))
        user_menu=menu.copy()
        if not  self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu']=user_menu

        context['cats']=cats

        if 'cat_selected' not in context:
            context['cat_selected']=0
        return context









         # if not cats:
         #     cats = Category.objects.annotate(Count('women'))
         #     cache.set('cats', cats, 60)
         # cats = Category.objects.all()
         # context['menu'] = menu
         # context['cats'] = cats
         # if 'cat_selected' not in context:
         #         context['cat_selected'] = 0
         # return context
