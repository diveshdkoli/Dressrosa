from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # register
    path('register/', views.register, name='register'),
    path("reg",views.reg,name='reg'),

    # login
    path('login_page/', views.login_page, name='login_page'),
    path('login_data',views.login_data,name='login_data'),
    path('logout_user', views.logout_user, name='logout_user'),

    # men
    path('men/',views.men,name='men'),

    # women
    path('women/', views.women, name='women'),

    # kids
    path('kids/', views.kids, name='kids'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # contact
    path('contact/', views.contact, name='contact'),

    #product_insert
    path('product_insert/',views.product_insert,name='product_insert'),

    #insert_data
    path('insert_data/',views.insert_data,name='insert_data'),

    #product list
    path('products/', views.product_list, name='product_list'),

    # product page
    path('product_page/<int:pid>/', views.product_page, name='product_page'),

    # product detail
    path('product/<int:pid>/', views.product_detail, name='product_detail'),


    # Cart URLs
    path('cart/', views.cart_page, name='cart_page'),
    path('cart/add/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),


   # forget password
    path('forget_pass/',views.forget_pass,name='forget_pass'),
]
