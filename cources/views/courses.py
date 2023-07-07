from email.policy import HTTP
from multiprocessing import context
from tempfile import TemporaryFile
from types import TracebackType

from django.shortcuts import render, redirect
from django.shortcuts import redirect, HttpResponse

from cources.models.course import Course, CourseProperty
from cources.models.user_course import UserCourse

from cources.models.video import Video

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import ListView


@method_decorator(login_required(login_url="login"), name="dispatch")
class MyCourseList(ListView):
    template_name = "courses/my_course.html"
    queryset =  UserCourse.objects.all()
    context_object_name= "user_course"

    def get_queryset(self):
        return UserCourse.objects.filter(user=self.request.user)
    
    
"""
@login_required(login_url="login")
def myCourse(request):
    user = request.user
    user_course = UserCourse.objects.filter(user=user)
    context = {
        "user_course": user_course
    }
    return render(request, "courses/my_course.html", context=context)
"""

def CoursePage(request, slug):
    course = Course.objects.get(slug=slug)
    serial_number = request.GET.get("lecture")
          
    if serial_number is None:
        serial_number = 1

    video = Video.objects.get(serial_number=serial_number, course=course)
    videos = course.video_set.all().order_by("serial_number")

    if video.is_preview is False:
        if request.user.is_authenticated is False:
            return redirect("login")
        else:
            user = request.user
            try:
                user_course = UserCourse.objects.get(user=user, course=course)
            except:
                return redirect("checkout", slug=course.slug)

    context = {
        "course": course,
        "video": video,
        "videos": videos
    }
    return render(request, "courses/course.html", context)
