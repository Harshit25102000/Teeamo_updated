from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
import datetime
User = get_user_model()
# Create your views here.
PRODUCT_PER_PAGE = 8


def index(request):
    featured_products = product.objects.filter(is_featured=True).order_by('-id')[:8]
    recent_products =  product.objects.all().order_by('-id')[:8]
    reviews=review.objects.all().order_by('-id')[:4]

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}


    context = {'featured_products':featured_products,'recent_products':recent_products,'reviews':reviews,'order':order}



    return render(request, 'teeamo/index.html',context)

def about(request):
    return render(request, 'teeamo/about.html')
def allproducts(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
    products = product.objects.all()
    ordering = request.GET.get('ordering', "")

    if ordering:
        products = product.objects.order_by(ordering)


    page = request.GET.get('page',1)

    product_paginator=Paginator(products, PRODUCT_PER_PAGE)
    try :
        products=product_paginator.page(page)
    except EmptyPage:
        products=product_paginator.page(product_paginator.num_pages)

    except:
        products=product_paginator.page(PRODUCT_PER_PAGE)
    data={'products':products, 'page_obj':products,'is_paginated':True,'paginator':product_paginator,
    'ordering':ordering, 'page':page,'order':order}



    return render(request, 'teeamo/products.html',data)

def searchresult(request):

    ordering = request.GET.get('ordering', "")
    search = request.GET.get('search', "")
    if search:
        products = product.objects.filter(Q(product_name__icontains=search) | Q(color__icontains=search))


    else:
        products = product.objects.all()

    if ordering:
        products = products.order_by(ordering)

    page = request.GET.get('page', 1)

    product_paginator = Paginator(products, PRODUCT_PER_PAGE)
    try:
        products = product_paginator.page(page)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)

    except:
        products = product_paginator.page(PRODUCT_PER_PAGE)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
    data = {'products': products, 'page_obj': products, 'is_paginated': True, 'paginator': product_paginator,
            'ordering': ordering, 'page': page, 'search':search,'order':order}



    return render(request, 'teeamo/searchresult.html', data)
    
def largeprints(request):

    page = request.GET.get('page', 1)
    products = product.objects.filter(category='Large Prints').order_by('-id')
    ordering = request.GET.get('ordering', "")
    if ordering:
        products = products.order_by(ordering)
    product_paginator = Paginator(products, PRODUCT_PER_PAGE)
    try:
        products = product_paginator.page(page)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)

    except:
        products = product_paginator.page(PRODUCT_PER_PAGE)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
    data = {'products': products, 'page_obj': products, 'is_paginated': True, 'paginator': product_paginator,
    'ordering':ordering,'order':order}

    return render(request, 'teeamo/largeprints.html', data)

def regularprints(request):


    page = request.GET.get('page', 1)
    products = product.objects.filter(category='Regular Prints').order_by('-id')
    ordering = request.GET.get('ordering', "")
    if ordering:
        products = products.order_by(ordering)
    product_paginator = Paginator(products, PRODUCT_PER_PAGE)
    try:
        products = product_paginator.page(page)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)

    except:
        products = product_paginator.page(PRODUCT_PER_PAGE)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
    data = {'products': products, 'page_obj': products, 'is_paginated': True, 'paginator': product_paginator,
    'ordering':ordering,'order':order}

    return render(request, 'teeamo/regularprints.html', data)



def tiedye(request):
    page = request.GET.get('page', 1)
    products = product.objects.filter(category='Tiedye').order_by('-id')
    ordering = request.GET.get('ordering', "")
    if ordering:
        products = products.order_by(ordering)
    product_paginator = Paginator(products, PRODUCT_PER_PAGE)
    try:
        products = product_paginator.page(page)
    except EmptyPage:
        products = product_paginator.page(product_paginator.num_pages)

    except:
        products = product_paginator.page(PRODUCT_PER_PAGE)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
    data = {'products': products, 'page_obj': products, 'is_paginated': True, 'paginator': product_paginator,
    'ordering':ordering,'order':order}

    return render(request, 'teeamo/tiedye.html', data)

def productdetail(request, id):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total': 0, 'get_cart_items':0,'shipping':False}


    products = product.objects.get(id=id)
    print(products)
    related_products = product.objects.filter(category=products.category).exclude(id=id)[:4]
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0,'shipping':False}
    return render(request, 'teeamo/productdetail.html',{'products':products, 'related':related_products,
    'order':order,'items':items})

def policy(request):
    return render(request, 'teeamo/policy.html')

def login(request):

    return render(request, 'teeamo/login.html')

def handlesignup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            messages.error(request, 'passwords do not match')
            return redirect('login')

        if '@' not in email:
            messages.error(request, 'Enter a valid email address')
            return redirect('login')
        siteuser=User.objects.create_user(email,password1)
        siteuser.save()
        messages.success(request,"Account created successfully")
        return redirect('Home')

    else:
        return HttpResponse('404 Not Allowed')

#from django.views.decorators.csrf import csrf_exempt

#@csrf_exempt
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        cart = json.loads(request.COOKIES['cart'])
        items=[]
        order={'get_cart_total': 0, 'get_cart_items':0,'shipping':False}

    context = {'items':items,'order':order}

    if request.user.is_authenticated:
        if order.get_cart_items == 0:
            return render(request, 'teeamo/emptycart.html')
        else:
            return render(request, 'teeamo/cart.html', context)
    else:
        if order['get_cart_items'] == 0:
            return render(request, 'teeamo/emptycart.html')
        else:
            return render(request, 'teeamo/cart.html', context)



#@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        items=[]
        order={'get_cart_total': 0, 'get_cart_items':0,'shipping':False}

    context = {'items':items,'order':order}
    return render(request,'teeamo/checkout.html',context)


def addtocart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            size = request.POST['size']
            quantity = request.POST['quantity']
            productid = request.POST['productid']
            customer = request.user
            products = product.objects.get(id=productid)

            order, created = Order.objects.get_or_create(customer=customer)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=products,size=size,quantity=quantity)
            orderItem.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        pass
#@csrf_exempt
def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action  = data['action']
    print('action',action)
    print('productId',productId)

    customer = request.user
    products= product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=products)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action =='delete':
        orderItem.quantity = 0
        
    orderItem.save()
    print("customer", customer)
    if orderItem.quantity<=0:
        orderItem.delete()
    return JsonResponse("item updated", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        total = data['formdata']['total']

        order.transaction_id= transaction_id

        if int(total) == order.get_cart_total :

            order.complete= True

        order.save()
        if data['formdata']['phone2'] == "":
            data['formdata']['phone2'] = "none"
        if data['formdata']['additionalinfo'] == "":
            data['formdata']['additionalinfo'] = "none"

        ShippingAddress.objects.create(
            customer= customer,
            name=data['formdata']['name'],
            email=data['formdata']['email'],
            order=order,
            phone1=data['formdata']['phone1'],
            phone2=data['formdata']['phone2'],
            address1=data['formdata']['address1'],
            address2=data['formdata']['address2'],
            city=data['formdata']['city'],
            state=data['formdata']['state'],
            pincode=data['formdata']['pincode'],
            date_added=datetime.datetime.now(),
            additionalinfo=data['formdata']['additionalinfo']


            )
    else:
        print('User is not loggen in.. ')
    return JsonResponse("payment complete", safe=False)