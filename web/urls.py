from django.urls import path
from .views import (
    ProductDetailView, 
    CategoryDetailView, 
    IndexView, 
    CartView, 
    AddProductToCartView, 
    ChangeQuantityView, 
    DeleteFromCartView, 
    CheckoutView,
    MakeOrderView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<str:ct_model>/<str:slug>', AddProductToCartView.as_view(), name='add_to_cart'),
    path('change_quantity/<str:ct_model>/<str:slug>', ChangeQuantityView.as_view(), name='change_quantity'),
    path('delete_from_cart/<str:ct_model>/<str:slug>', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make_order/', MakeOrderView.as_view(), name='make_order')
]