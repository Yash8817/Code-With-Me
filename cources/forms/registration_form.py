from dataclasses import field
from operator import truediv
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError

class Registration(UserCreationForm):
    first_name = forms.CharField( max_length=20, required=True)
    last_name = forms.CharField( max_length=20, required=True)
    email =forms.EmailField(required=True )
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password1","password2"]
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        user = None
        try:
            user = User.objects.get(email = email)
        except:
            return email
        
        if user is not None:
            raise ValidationError("Email already exists")


