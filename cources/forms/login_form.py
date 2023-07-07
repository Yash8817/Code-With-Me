from dataclasses import field
from operator import truediv
from pyexpat import model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, login
from django.forms import ValidationError


class LoginForm(AuthenticationForm):
    username = forms.EmailField(required=True, label="Email Address")

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = None
        try:
            user = User.objects.get(email=email)
            result = authenticate(username=user.username, password=password)

            if result is not None:
                return result

            else:
                raise ValidationError("Email or Password invalid!")
        except:
            raise ValidationError("Email or Password invalid!")
        
