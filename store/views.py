from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.models import User
import json
from cart.cart import Cart
from payment.models import ShippingAddress
from payment.forms import ShippingForm
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm

# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'home.html', context)

def about(request):
    context ={}
    return render(request, 'about.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                #Do some shoopping  cart stuff
                current_user = Profile.objects.get(user__id=request.user.id)
                saved_cart = current_user.old_cart
                if saved_cart:
                    #convert to dict using JSON
                    converted_cart= json.loads(saved_cart)
                    #Add the loaded cart dict to our session
                    cart = Cart(request)
                    #Loop through the cart and add the items from the database
                    for key,value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)



                messages.success(request, "You have been logged in!")
                return redirect('home')
            messages.error(request, "Invalid Credentials")
            return redirect('login')
            
        messages.error(request, "Fill in all fields")
        return redirect('login')
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out....Thanks for coming by")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(request, username=username, password=password)
            login(request,user)
            messages.success(request, "Username Created - Please fill your User Info Below")
            return redirect('update_info')
        messages.error(request, "There was a problem registering, Try again")
        return redirect('register')
    return render(request, 'register.html' ,{'form':form})

def product(request, pk):
    product = Product.objects.get(id =pk)
    context = {
        'product':product
    }
    return render(request, 'products.html',context)

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name = foo)
        products = Product.objects.filter(category =category)
        context = {
        'product':products,
        'category':category
        }
        return render(request, 'category.html',context)
    except:
        messages.error(request, "Category doesn't exist")
        return redirect('home')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, "category_summary.html",{'categories':categories})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id =request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User has been Updated!!")
            return redirect('home')
        return render(request, "update_user.html", {'user_form':user_form})
    
    messages.error(request, "You must be logged in to access the page")
    return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password has been updated successfull")
                login(request, current_user)
                return redirect('update_password')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
            
        else:
            form = ChangePasswordForm(current_user)
            return render(request,'update_password.html', {'form':form})
    messages.success(request, "You must be logged in to view that page")
    return redirect('home')
    
def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id =request.user.id)
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)
        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance = shipping_user)
        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
           
            messages.success(request, "You Info has been Updated!!")
            return redirect('home')
        return render(request, "update_info.html", {'form':form, 'shipping_form':shipping_form})
    
    messages.error(request, "You must be logged in to access the page")
    return redirect('home')