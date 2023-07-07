from email.policy import HTTP
from multiprocessing import context
from operator import ipow
from django.shortcuts import render, redirect
from django.shortcuts import redirect, HttpResponse
from cources.models.course import Course, CourseProperty
from cources.models.video import Video
from cources.forms import Registration, LoginForm
from django.views import View
from django.contrib.auth import logout ,login
from django.views.generic.edit import FormView

class SignUpView(FormView):
    template_name =  "courses/signup.html"
    form_class = Registration
    success_url = "/login"

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)



"""
class SignUpView(View):
    def get(self, request):
        form = Registration()
        return render(request, "courses/signup.html", {"form": form})

    def post(self, request):
        form = Registration(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect("login")

        return render(request, "courses/signup.html", {"form": form})
"""



class LoginView(FormView):
    template_name =  "courses/login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        login(self.request, form.cleaned_data)
        next_page = self.request.GET.get("next")
        if next_page is not None:
            return redirect(next_page)
        
        
        return super().form_valid(form)
"""
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, "courses/login.html", context=context)

    def post(self, request):
        form = LoginForm(request=request, data=request.POST)
        context = {
            "form": form
        }
        if (form.is_valid()):
            return redirect("home")
        else:
            return render(request, "courses/login.html", context=context)
"""




def signout(request):
    logout(request)
    return redirect("home")