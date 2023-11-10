from django.shortcuts import render, redirect
from app.models import Catalog, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.views.generic import ListView

def home(request):
    if request.method == 'GET':
        if Catalog.objects.filter(owner=request.user) != None:
            return redirect('/add-products/')
        else: 
            return render(request, 'homepage.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        if Catalog.objects.filter(owner=request.user) != None:
            return redirect('/add-products/')
        else: 
            return render(request, 'homepage.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'signin.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('/')

def create_catalog(request):
    if request.method == 'POST':
        catalog_name = request.POST.get('catalog_name')
        catalog_slug = request.POST.get('catalog_slug')

        catalog_object = Catalog.objects.create(name=catalog_name, slug=catalog_slug, owner=request.user)

        if catalog_object:
            return redirect('/add-products/')
        
def add_products(request):
    if request.method == 'POST':
        current_catalog = Catalog.objects.filter(owner=request.user)[0]
        catalog_slug = current_catalog.slug
        
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_description = request.POST.get('product_description')

        product_object = Product.objects.create(product_name=product_name, product_price=product_price, product_description=product_description, under_catalog=current_catalog)

        if product_object:
            return redirect('/catalog/{0}'.format(catalog_slug))
    return render(request, 'add_products.html')

def product_list_view(request, slug):
        current_catalog = Catalog.objects.filter(slug=slug)[0]
        product_set = Product.objects.filter(under_catalog=current_catalog)

        return render(request, 'view_products.html', {'products':product_set})