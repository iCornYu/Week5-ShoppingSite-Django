from django.db.models.fields.related import ForeignKey
from django.shortcuts import render, redirect
from .models import Product, Cart
from .forms import CustomUserForm, CartForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404 
from django.db.models import Sum




# Create your views here.
def indexPage(request):
    return render(request, 'shop/index.html')

def productsPage(request):
    products = Product.objects.all()
    context = {'products' : products}
    return render(request, 'shop/products.html', context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            print(f'{user} is logged in.')
            return redirect('shop-index')
        messages.info(request, "Incorrect username or password. Please try again.")
    return render(request, 'shop/login.html')

def registerPage(request):
    form = CustomUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        context = {"user" : user }
        template = render_to_string('shop/emailmessage.html', context)
        email_message = EmailMessage(
            "Welcome to BuildaPC!",
            template, 
            settings.EMAIL_HOST_USER,
            [email], 
        )
        email_message.fail_silently = False
        email_message.send()
        messages.success(request,"Account was successfully created for " + user)
        return redirect('shop-login')
    context = {'form' : form}
    return render(request,'shop/register.html', context)

@login_required(login_url = 'shop-login')
def logoutPage(request):
    logout(request)
    return redirect('shop-login')

def singleProduct(request, product_id):
    individual = Product.objects.get(product_id=product_id)
    context = {'p':individual}
    return render(request, 'shop/individual.html', context)


@login_required(login_url = 'shop-login')
def deleteCart(request, cart_id):
    product = Cart.objects.get(cart_id=cart_id)
    product.delete()
    messages.success(request, "The item has been successfully deleted.")
    return redirect('shop-cart')

@login_required(login_url = 'shop-login')
def addCart(request):
    cart = CartForm(request.POST)
    if cart.is_valid():
        cart.save()
    messages.success(request, "Added to cart.")
    return redirect('shop-products')


@login_required(login_url = 'shop-login')
def myCart(request):
    cart = Cart.objects.filter(username=request.user.id)
    # products = Cart.objects.all().values_list('product_id', flat=True)
    # for x in products:
    #     price = Product.objects.filter(product_id=x).values('price')
    
    # sum = Product.objects.filter(pk__in=products).aggregate(Sum('price'))
    context = {'cart' : cart}

    return render(request, 'shop/cart.html', context)




    