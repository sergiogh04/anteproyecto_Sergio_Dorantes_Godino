from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# yourapp/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido. Ingresa un correo válido.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
