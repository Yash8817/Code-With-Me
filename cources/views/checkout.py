from email.policy import HTTP
from multiprocessing import context
import logging
from django.shortcuts import render, redirect
from django.shortcuts import redirect, HttpResponse


from cources.models.course import Course, CourseProperty 
from cources.models.payment import Payment
from cources.models.user_course import UserCourse
from cources.models.video import Video

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from codewithme import settings
from time import time

import razorpay
client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRATE))


@login_required(login_url="/login")
def CheckOut(request, slug):

    course = Course.objects.get(slug=slug)
    
    user = request.user
    order = None
    payment = None
    error = None
    receipt = ""
    action = request.GET.get("action")
    if action == "make_payment":

        try:
            user_course  = UserCourse.objects.get(user = user , course = course)
            error = "You are already enrolled in this course!"
        except:
            amount = int((course.price - (course.price * course.discount * 0.01)) * 100)

        if amount == 0 :
            usercouse = UserCourse(user = user , course = course )
            usercouse.save()
            return redirect("myCourse")

        elif error is None :
            amount = amount
            currency = "INR"
            notes = {
                "email": user.email,
                "fname": user.first_name,
                'user': f'{user.first_name} {user.last_name}'
            }
            receipt = f"codewithme-{int(time())}"

            data = {"amount": amount, "currency": currency,
                    "receipt": receipt, "notes": notes}
            order = client.order.create(data=data)

            payment  = Payment()
            payment.order_id = order.get("id")
            payment.user = user
            payment.course = course
            payment.save()

    context = {
        "course": course,
        'order': order,
        "payment": payment,
        "user": user , 
        "error": error
    }


    return render(request, "courses/checkout.html", context)



@csrf_exempt
def verifyPayment(request):
    if request.method == "POST":
        mydata = request.POST    
        data = dict(mydata)
        
        context ={}
        try:

            client.utility.verify_payment_signature(mydata)
            razorpay_by_order_id = data['razorpay_order_id']
            razorpay_order_id = razorpay_by_order_id[0]

            razorpay_payment_by_id = data['razorpay_payment_id']
            razorpay_payment_id = razorpay_payment_by_id[0]
            
            payment = Payment.objects.get( order_id = razorpay_order_id)

            print("payment " , payment)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            usercouse = UserCourse(user = payment.user , course = payment.course )
            print(razorpay_order_id)
            usercouse.save()

            payment.user_course = usercouse

            payment.save()

            return redirect("myCourse")

        except Exception as e:
            return HttpResponse(e)



        
    
