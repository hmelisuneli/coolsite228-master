from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .forms import *
from .models import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializer import HeroSerializer
from .utils import *

class HeroHome(DataMixin, ListView):
    paginate_by = 3
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True)




def index(request):
  posts = Women.objects.all()

  context = {
      'posts': posts,
     'menu': menu,
      'title': 'Главная страница',
       'cat_selected': 0,
   }

  return render(request, 'women/marvel.html', context=context)

def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get('page')
    page_obj =  paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj':page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Панель админа")
        return dict(list(context.items()) + list(c_def.items()))


#def addpage(request):
 #   if request.method == 'POST':
  #      form = AddPostForm(request.POST, request.FILES)
   #     if form.is_valid():
    #        #print(form.cleaned_data)
     #       try:
      #          form.save()
       #         return redirect('home')
        #    except:
         #       form.add_error(None, 'Ошибка добавления поста')
#
 #   else:
  #      form = AddPostForm()
   # return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})


#def contact(request):
 #   return HttpResponse("Обратная связь")




class ContactFormView(DataMixin, FormView):
     form_class = ContactForm
     template_name = 'women/contact.html'
     success_url = reverse_lazy('home')

     def get_context_data(self, object_list=None,  **kwargs):
         context = super().get_context_data(**kwargs)
         c_def = self.get_user_context(title="Обратная связь")
         return dict(list(context.items()) + list(c_def.items()))

     def form_valid(self, form):
         print(form.cleaned_data)
         return redirect('home')



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def show_post(request, post_slug):
   post = get_object_or_404(Women, slug=post_slug)

   context = {
      'post': post,
     'menu': menu,
    'title': post.title,
   'cat_selected': post.cat_id,
}

   return render(request, 'women/post.html', context=context)



class HeroCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c=Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items())+list(c_def.items()))

#def show_category(request, cat_id):
#    posts = Women.objects.filter(cat_id=cat_id)
#
 #   if len(posts) == 0:
  #      raise Http404()
#
 #   context = {
  #      'posts': posts,
   #     'menu': menu,
    #    'title': 'Отображение по рубрикам',
     #   'cat_selected': cat_id,
    #}#

    #return render(request, 'women/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))



class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name ='women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')

class Person(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField()

    def index(request):
        people = Women.objects.all()
        return render(request, "index.html", {"people": people})

    # сохранение данных в бд
    def create(request):
        if request.method == "POST":
            person = Women()
            person.name = request.POST.get("name")
            person.age = request.POST.get("age")
            person.save()
        return HttpResponseRedirect("/")

    # изменение данных в бд
    def edit(request, id):
        try:
            person = Women.objects.get(id=id)

            if request.method == "POST":
                person.name = request.POST.get("name")
                person.age = request.POST.get("age")
                person.save()
                return HttpResponseRedirect("/")
            else:
                return render(request, "edit.html", {"person": person})
        except Person.DoesNotExist:
            return HttpResponseNotFound("<h2>Person not found</h2>")

    # удаление данных из бд
    def delete(request, id):
        try:
            person = Person.objects.get(id=id)
            person.delete()
            return HttpResponseRedirect("/")
        except Person.DoesNotExist:
            return HttpResponseNotFound("<h2>Person not found</h2>")


class HeroAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 3

class HeroAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = HeroSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class HeroAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = HeroSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,)

class HeroAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = HeroSerializer
    permission_classes = (IsAdminOrReadOnly, )


# class HeroViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,GenericViewSet):
#    # queryset = Women.objects.all()
#    serializer_class = HeroSerializer
#
#    def get_queryset(self):
#        pk =self.kwargs.get("pk")
#
#        if not pk:
#            return Women.objects.all()[:3]
# #       return Women.objects.filter(pk=pk)
#    @action(methods=['get'], detail=False)
#    def Categoty(self, request, pk=None):
#        cats = Category.objects.all(pk=pk)
#        return Response({'cats':[c.name for c in cats]})
#
#
#
#



# class HeroAPIList(generics. ListCreateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = HeroSerializer
#
# class HeroAPIUpdate(generics.UpdateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = HeroSerializer
#
# class HeroAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Women.objects.all()
#     serializer_class = HeroSerializer

# class HeroAPIView(APIView):
#     def get(self, requset):
#         w = Women.objects.all()
#         return Response({'posts': HeroSerializer(w, many=True).data})
#
#     def post(self, requset):
#         serializer = HeroSerializer(data=requset.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#       pk = kwargs.get("pk", None)
#       if not pk:
#             return  Response({"error": "Method PUT not allowed"})
#
#       try:
#             instance = Women.obects.get(pk=pk)
#       except:
#             return Response({"error": "Object does not exist"})
#
#       serializer = HeroSerializer(data=request.data, instance=instance)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#         instance.delete()
#
#         return Response({"post": "delete post " + str(pk)})
#

# class HeroAPIView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = HeroSerializer