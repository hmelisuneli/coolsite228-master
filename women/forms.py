from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import *

class AddPostForm(forms.ModelForm):
  class Meta:
      model = Women
      fields = ['title','slug','content','photo','is_published','cat']
      widgets = {
          'title' : forms.TextInput(attrs={'class':'form-input'}),
          'content' : forms.Textarea(attrs={'cols': 60,'rows': 10}),
      }

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'form-input'}),
            'password1' : forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2' : forms.PasswordInput(attrs={'class': 'form-input'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()