# Views.py in shop app
import decimal
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from . import models
from cart.forms import CartAddProductForm
from cart.cart import Cart
import requests
import json


# Index function
def index(request):
    product_list = models.Product.objects.all()[:5]
    return render(request, 'index.html', {'product_list': product_list})


# Checkout function
@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        order = models.Order.objects.create(customer=request.user)
        for item in cart:
            models.OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            product_price=item['price'],
                                            product_count=item['product_count'],
                                            product_cost=Decimal(item['product_count']) * Decimal(item['price']))
        order.customer = request.user
        order.save()
        cart.clear()
        return render(request, 'order_detail.html', {'order': order})
    return render(request, 'checkout.html', {'cart': cart})


# Product function
def product(request, pk):
    product_detail = get_object_or_404(models.Product, id=pk)
    cart_add_product_form = CartAddProductForm()
    return render(request, 'product.html', {'product_detail': product_detail,
                                            'cart_add_product_form': cart_add_product_form})


# Store function
def store(request):
    return render(request, 'store.html')


# DecimalEncoder class
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


# Create variables for to_bank function
MERCHANT = '*************************************'
ZP_API_REQUEST = 'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/request.json'
ZP_API_VERIFY = 'https://sandbox.banktest.ir/zarinpal/api.zarinpal.com/pg/v4/payment/verify.json'
ZP_API_STARTPAY = 'https://sandbox.banktest.ir/zarinpal/www.zarinpal.com/pg/StartPay/{authority}'
callbackurl = 'http://127.0.0.1:8000/callback/'
mobile = '0213124'
email = 'test@gmail.com'
description = 'Test'
amount = 0


def to_bank(request, order_id, amount=amount):
    order = get_object_or_404(models.Order, id=order_id)
    order_items = models.OrderItem.objects.filter(order=order)
    for item in order_items:
        amount += item.product_cost
    req_data = {
        "merchant_id": MERCHANT,
        "amount": amount,
        "callback_url": callbackurl,
        "description": description,
        "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data, cls=DecimalEncoder), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


# Verify function
def verify(request, order_id, amount=amount):
    order = get_object_or_404(models.Order, id=order_id)
    order_items = models.OrderItem.objects.filter(order=order)
    for item in order_items:
        amount += item.product_cost
    t_authority = request.GET['authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "callback_url": callbackurl,
            "description": description,
            "metadata": {"mobile": mobile, "email": email}
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data, cls=DecimalEncoder), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return HttpResponse('Transaction success.\nRefID: ' + str(
                    req.json()['data']['ref_id']
                ))
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')


# Callback function
def callback(request, amount=amount):
    if request.GET.get('Status') == 'OK':
        authority = request.GET.get('authority')
        invoice = get_object_or_404(models.Invoice, authority=authority)
        order = invoice.order
        order_items = models.OrderItem.objects.filter(order=order)
        for item in order_items:
            amount += item.product_cost
        if request.method == 'POST':
            r = requests.post(ZP_API_REQUEST, params=request.POST)
        else:
            r = requests.post(ZP_API_REQUEST, params=request.POST)
        if r.status_code == 200:
            return render(request, 'callback.html', {'invoice': invoice})
    else:
        return HttpResponse('Operation is faild')
