from email.policy import HTTP

from django.shortcuts import render
from django.shortcuts import redirect  , HttpResponse
from cources.models import Course

from django.views.generic import ListView

class CourseList(ListView):
    template_name="courses/homepage.html"
    queryset =Course.objects.filter(active = True)
    context_object_name = 'courses'
    
"""
def home(request):
    courses = Course.objects.all()
    return render(request , "courses/homepage.html" , {'courses':courses})
"""