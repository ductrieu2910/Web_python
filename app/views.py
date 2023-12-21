from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
#detail
def contact(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    if request.method == "POST":
        user_not_login ="hidden"
        user_login = "show"
    else:
        user_not_login ="show"
        user_login = "hidden"
    context = {'categories':categories,'active_category':active_category,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/contact.html',context)
def introduce(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    if request.method == "POST":
        user_not_login ="hidden"
        user_login = "show"
    else:
        user_not_login ="show"
        user_login = "hidden"
    context = {'categories':categories,'active_category':active_category,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/introduce.html',context)
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login ="hidden"
        user_login = "show"
    else:
        items =[]
        order ={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login ="show"
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub=False)
    context={'categories':categories,'products':products,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/detail.html',context)

def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    if request.user.is_authenticated:
        user_not_login ="hidden"
        user_login = "show"
    else:
        user_not_login ="show"
        user_login = "hidden"
    discount_products = Product.objects.filter(is_discounted=True)
    all_products = Product.objects.filter(is_discounted=False)
    products = Product.objects.all()
     # Phân trang cho sản phẩm giảm giá
    page_discount = request.GET.get('page_discount', 1)
    paginator_discount = Paginator(discount_products, 4)  # Hiển thị 4 sản phẩm trên mỗi trang
    try:
        discount_products = paginator_discount.page(page_discount)
    except PageNotAnInteger:
        discount_products = paginator_discount.page(1)
    except EmptyPage:
        discount_products = paginator_discount.page(paginator_discount.num_pages)

        # Phân trang cho tất cả sản phẩm
    page_all = request.GET.get('page_all', 1)
    paginator_all = Paginator(all_products, 4)
    try:
        paginated_all_products = paginator_all.page(page_all)
    except PageNotAnInteger:
        paginated_all_products = paginator_all.page(1)
    except EmptyPage:
        paginated_all_products = paginator_all.page(paginator_all.num_pages)
    context = {'categories':categories,'discount_products': discount_products,'all_products': paginated_all_products,'products':products,'active_category':active_category,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/category.html',context)  
 
def search(request):
    if request.method =="POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains= searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login ="hidden"
        user_login = "show"
    else:
        items =[]
        order ={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']  
        user_not_login ="show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
    context= {'categories':categories,'searched':searched,'keys':keys,'products': products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render (request,'app/search.html',context)

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        user_not_login ="hidden"
        user_login = "show"
    else:
        user_not_login ="show"
        user_login = "hidden"
        if form.is_valid():
            form.save()
            return redirect('login')
    categories = Category.objects.filter(is_sub=False)
    context = {'categories':categories,'form':form,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        user_not_login ="hidden"
        user_login = "show"
        return redirect('home')
    else:
        user_not_login ="show"
        user_login = "hidden"
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username =username,password =password)
        if user is not None:
            login(request,user)
            return redirect('home')
            
        else:
            messages.info(request,'user or password not correct!')
    categories = Category.objects.filter(is_sub=False)
    context ={'categories':categories,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login ="hidden"
        user_login = "show"
    else:
        items =[]
        order ={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login ="show"
        user_login = "hidden"
    all_products = Product.objects.filter(is_discounted=False)
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
     # Lọc sản phẩm giảm giá và tất cả sản phẩm
    discount_products = Product.objects.filter(is_discounted=True)
    all_products = Product.objects.filter(is_discounted=False)
    # Phân trang cho sản phẩm giảm giá
    page_discount = request.GET.get('page_discount', 1)
    paginator_discount = Paginator(discount_products, 4)  # Hiển thị 4 sản phẩm trên mỗi trang
    try:
        discount_products = paginator_discount.page(page_discount)
    except PageNotAnInteger:
        discount_products = paginator_discount.page(1)
    except EmptyPage:
        discount_products = paginator_discount.page(paginator_discount.num_pages)

        # Phân trang cho tất cả sản phẩm
    page_all = request.GET.get('page_all', 1)
    paginator_all = Paginator(all_products, 4)
    try:
        paginated_all_products = paginator_all.page(page_all)
    except PageNotAnInteger:
        paginated_all_products = paginator_all.page(1)
    except EmptyPage:
        paginated_all_products = paginator_all.page(paginator_all.num_pages)
    context= {'categories':categories,'discount_products': discount_products,'all_products': paginated_all_products,'products': products,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/home.html',context)

@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login ="hidden"
        user_login = "show"
    else:
        items =[]
        order ={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login ="show"
        user_login = "hidden"
    # Thêm giá giảm giá vào mỗi item trong giỏ hàng
    for item in items:
        if item.product.is_discounted:
            item.discounted_price = item.product.get_discounted_price()

    # Lấy giá giảm giá từ sản phẩm
    discounted_price = 0
    for item in items:
        discounted_price += item.discounted_price    
        discounted_total = order.discounted_total
    size = request.POST.get('size')
    categories = Category.objects.filter(is_sub=False)
    context={'size':size,'categories':categories,'discounted_price': discounted_price,'discounted_total': discounted_total,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer =customer,complete= False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login ="hidden"
        user_login = "show"
    else:
        items =[]
        order ={'get_cart_items':0,'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login ="show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context={'categories':categories,'items':items,'order':order,'cartItems':cartItems,'user_not_login':user_not_login,'user_login':user_login}
    return render(request,'app/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer =customer,complete= False)
    orderItem, created = OrderItem.objects.get_or_create(order = order,product= product)
    if action =='add':
        orderItem.quantity +=1
    elif action =='remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse('added',safe =False)