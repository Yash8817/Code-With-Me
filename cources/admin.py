from atexit import register
import math
from django.utils.html import format_html
from pyexpat import model
from django.contrib import admin
from cources.models import Course, Tag, payment, prerequisite, learning, Video, UserCourse, Payment


# Register your models here.


class TagAdmin(admin.TabularInline):
    model = Tag


class PrereuisiteAdmin(admin.TabularInline):
    model = prerequisite


class LearningAdmin(admin.TabularInline):
    model = learning


class VideoAdmin(admin.TabularInline):
    model = Video


class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin, PrereuisiteAdmin, LearningAdmin, VideoAdmin]
    list_display = ["name", "my_price", "my_discount",
                    "final_Price", "active", "View_on_web"]
    list_filter = ["price", "discount", "active", "date"]

    def my_price(self, course):
        return f"₹ {course.price}"
    my_price.short_description = "Price"

    def my_discount(self, course):
        return f"{course.discount}%"
    my_discount.short_description = "Discount"

    def final_Price(self, course):
        sellprice = course.price - (course.price * course.discount * 0.01)
        return f"₹  {math.floor(sellprice)}"

    def View_on_web(self, course):
        return format_html(f"<a target='_blank'  href='/course/{course.slug}' >View on web </a>")


class PaymentAdmin(admin.ModelAdmin):
    model = Payment
    list_display = ["order_id",  "get_user", "get_course", "status"]
    list_filter = ["course", "date", "status"]

    def get_user(self, Payment):
        return format_html(f"<a  target='_blank' href='/admin/auth/user/{Payment.user.id}'>{Payment.user}</a>")
    get_user.short_description = "User"

    def get_course(self, Payment):
        return format_html(f"<a  target='_blank' href='/admin/cources/course/{Payment.course.id}'>{Payment.course}</a>")
    get_course.short_description = "Course"


class UserCourseAdmin(admin.ModelAdmin):
    model = UserCourse
    list_display = ["OrderDetail", "get_user", "get_course"]
    list_filter = ["course"]

    def OrderDetail(self, UserCourse):
        return format_html(f"<a  href='/admin/cources/usercourse/{UserCourse.id}'>Open</a>")
    OrderDetail.short_description = "Order Detail"

    def get_user(self, UserCourse):
        return format_html(f"<a  target='_blank' href='/admin/auth/user/{UserCourse.user.id}'>{UserCourse.user}</a>")
    get_user.short_description = "User"

    def get_course(self, UserCourse):
        return format_html(f"<a  target='_blank' href='/admin/cources/course/{UserCourse.course.id}'>{UserCourse.course}</a>")
    get_course.short_description = "Course"

class VideoAdmin(admin.ModelAdmin):
    model= Video
    list_display= [ "title","course" ,"is_preview"]
    list_filter= ["course" , "is_preview"]


admin.site.register(Course, CourseAdmin)
admin.site.register(Video ,VideoAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(Payment,  PaymentAdmin)
