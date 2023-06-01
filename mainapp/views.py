from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from .models import *
import random
import datetime

import json
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
# Create your views here.
from django.core.mail import send_mail


email_txt = """Здравствуйте! Ваш заказ принят! 
По поводу завершения оформления и оплаты обратитесь к одному из наших администраторов в Телеграмм:  @BK1LUV / @flwth3 / @XxOpKf
При обращении присылайте ID своего заказа. ID вашего заказа: """




def home(request):
    return render(request, 'home.html', {})

def home_redir(request):
    return redirect(home)

def callback(request):
    return redirect(home)

def account_logout_redir(request):
    
    return redirect(profile)


def about(request):
    return render(request, 'about.html', {})



@login_required(login_url='profile')
def blog(request):
    if request.method == "POST":
        
        text = request.POST.get('text', False)
        date = request.POST.get('date', False)
        image = request.FILES.get('image', False)
        object = Post.objects.create(author=request.user, text=text, date=date, image=image)
        object.save()
        return redirect("/blog")
    else:
        form = PostForm()
    messages = Post.objects.all()

    return render(request, 'blog.html', {'messages': messages, 'form': form})




def profile(request):
    return render(request, 'profile.html', {})



def product(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product':product})
    


def shop(request):
    products = Product.objects.all()

    if request.user.is_authenticated:
        customer = request.user
        try:
            order, created = Order.objects.get_or_create(customer=customer, completed=False)
        except Order.MultipleObjectsReturned:
            order= Order.objects.filter(customer=customer).first()
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    return render(request, 'shop.html', {'products':products,  'cartItems':cartItems})



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    try:
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
    except Order.MultipleObjectsReturned:
        order= Order.objects.filter(customer=customer, completed=False).first()
    try:
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    except OrderItem.MultipleObjectsReturned:
        orderItem = OrderItem.objects.filter(order=order, product=product).first()
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)

@login_required
def cart(request):

    if request.user.is_authenticated:
        customer = request.user
        try:
            order, created = Order.objects.get_or_create(customer=customer, completed=False)
        except Order.MultipleObjectsReturned:
            order= Order.objects.filter(customer=customer, completed=False).first()
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    return render(request, 'cart.html', {'items':items, 'order':order, 'cartItems':cartItems})

@login_required
def checkout(request):
    return render(request, 'checkout.html', {})



def success(request):
    customer = request.user
    order = Order.objects.get(customer=customer, completed=False)
    order.completed=True
    order.transaction_id = datetime.datetime.now().timestamp()
    order.save()


    # Отправка email
    # вида: to-subject-text !!!
    msg_subject = "Ваш заказ принят ГАМБАМом."
    msg_text = email_txt + f'{str(order.transaction_id)}. \nУдачи!'
    send_mail(msg_subject, msg_text, 'gambam-community@yandex.ru', [str(request.user.email)], fail_silently=False)


    return render(request, 'success.html', {'user':customer})


def galery(request):
    pictures = Picture.objects.all()
    return render(request, 'galery.html', {'pictures':pictures})