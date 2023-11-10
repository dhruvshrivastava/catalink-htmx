from django.urls import path 
from app import views

urlpatterns = [
     path("signin/", views.signin),
     path("signup/", views.signup),
     path("signout/", views.signout),
     path("create-catalog/", views.create_catalog),
     path("add-products/", views.add_products),
     path("catalog/<slug:slug>", views.product_list_view),
     path("", views.home)
]