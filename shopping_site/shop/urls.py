from django.urls import path
from . import views


urlpatterns = [
    path('', views.indexPage, name='shop-index'),
    path('index/', views.indexPage, name='shop-index'),
    path('products/', views.productsPage, name='shop-products'),
    path('login/', views.loginPage, name='shop-login'),
    path('register/', views.registerPage, name= 'shop-register'),
    path('logout/', views.logoutPage, name= 'shop-logout'),
    path('products/<int:product_id>', views.singleProduct, name='shop-individual'),
    path('cart/', views.myCart, name='shop-cart'),
    path('products/add/', views.addCart, name='shop-cartupdate'),
    path('products/delete/<int:cart_id>', views.deleteCart, name='shop-cartdelete'),


]