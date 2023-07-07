from atexit import register
from dis import disco
from django import template
import math
from cources.models import UserCourse , Course
from django.utils.html import format_html
register = template.Library()


@register.simple_tag
def cal_sell_price(price , discount):
    sellprice = 0
    #if discount is not availablr then return the original price
    if discount is None or discount == 0:
        return price
    
    #calculate the discount and return the discount
    sellprice = price - ( price * discount * 0.01 )
    return math.floor(sellprice)



#add rupee symbo
@register.filter
def rupee(price):
    return f'₹{price}'



@register.simple_tag
def is_enrolled(request , course):
    isenrolled = False
    if request.user.is_authenticated is False:
        return False
    user = request.user
    try:
        user_course  = UserCourse.objects.get(user = user , course = course)
        return True
    except:
        return False

