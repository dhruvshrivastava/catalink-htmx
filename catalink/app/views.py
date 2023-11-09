from django.shortcuts import render, redirect
from app.models import Catalog
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse

def home(request):
    if request.method == 'GET':
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
    return HttpResponse('Dummy for adding products')