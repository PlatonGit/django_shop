from django.db import models


def recalc_cart_fin_price(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'), models.Sum('quantity'))
    if cart_data.get('final_price__sum') is not None:
        cart.final_price = cart_data.get('final_price__sum')
    else: 
        cart.final_price = 0
    cart.total_products = cart_data.get('quantity__sum')
    cart.save()