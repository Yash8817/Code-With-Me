
from django.contrib import admin
from django.urls import path
from cources.views import CourseList, CoursePage, LoginView, SignUpView , signout , CheckOut  , MyCourseList
from cources.views.checkout import verifyPayment 
from django.conf.urls.static import static
from codewithme.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('', CourseList.as_view()  , name="home"),
    path('login', LoginView.as_view(), name="login"),
    path('signup', SignUpView.as_view(), name="signup"),
    path('logout', signout , name="logout"),
    path('course/<str:slug>', CoursePage, name="CoursePage"),
    path('myCourse', MyCourseList.as_view() , name="myCourse"),
    path('checkout/<str:slug>', CheckOut, name="checkout"),
    path('verify_payment', verifyPayment, name="verify_payment"),
    
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
