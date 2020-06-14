from django.http import JsonResponse
from django.shortcuts import render

from house.models import House
from order.models import Order
from user import login_test

# Create your views here.


@login_test.login
def order(request):
    userid = request.session.get("user_id")
    orders = Order.objects.filter(user_id=userid)
    return render(request, "order/my_order.html", locals())


@login_test.login
def addorder(request, hid, num):
    msg = {}
    user_id = request.session.get("user_id")
    if Order.objects.filter(house_id=hid, user_id=user_id):
        order = Order.objects.get(house_id=hid)
        order.delete()
    else:
        price = House.objects.get(pk=hid).price
        amount = int(price) * int(num)
        Order.objects.create(
            house_id=hid,
            user_id=user_id,
            days=num,
            house_price=price,
            amount=amount,
            status="0",
        )
        msg["code"] = 400
        msg["msg"] = "预约成功"
    return JsonResponse(msg)
