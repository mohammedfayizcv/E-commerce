from email.message import EmailMessage
from django.shortcuts import render
from django.template import context
from django.http import JsonResponse
import json
from .models import *
from .utils import cookieCart,cartData,guestOrder
import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def funStore(request):

    data=cartData(request)
    cartItems=data['cartItem']

    products = Product.objects.all()
    context = {'product': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def funCart(request):

    data=cartData(request)
    cartItems=data['cartItem']
    order=data['order']
    items=data['items']
       
            
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def funCheckOut(request):
   
    data=cartData(request)
    cartItems=data['cartItem']
    order=data['order']
    items=data['items']
        
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    Data = json.loads(request.body)
    productId = Data['productId']
    action = Data['action']
    print('proid:', productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
       
    else:
        customer,order=guestOrder(request,data)
        
  
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

        
    return JsonResponse('payment complete', safe=False)
