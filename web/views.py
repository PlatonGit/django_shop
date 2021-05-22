from django.db import transaction
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.views.generic import DetailView, View
from django.contrib import messages
from .models import *
from .mixins import CategoryDetailMixin, CartMixin
from .forms import OrderForm
from .utils import recalc_cart_fin_price


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'categories': Category.objects.get_categories_for_left_sidebar(),
            'products': LatestProducts.objects.get_products_for_main_page('notebook', 'smartphone', 'smarttv', 'headphones', with_respect_to='notebook', count=(2, 2, 2, 2))
        }
        return render(request, 'base.html', context)


# def index(request):
#     # print(request.GET)
#     # print(request.POST)
#     # product = Notebook.objects.all()[0]
#     return render(request, 'base.html', {'categories': Category.objects.get_categories_for_left_sidebar()})


class ProductDetailView(CategoryDetailMixin, DetailView):
    
    CT_MODEL_MODEL_CLASS = {
        'notebook' : Notebook,
        'smartphone' : Smartphone,
        'smarttv' : SmartTV,
        'headphones' : Headphones
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)
    
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        return context
    

class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
            'categories':  Category.objects.get_categories_for_left_sidebar()
        }
        return render(request, 'cart.html', context)


class AddProductToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        
        ct_model = kwargs.get('ct_model')
        slug = kwargs.get('slug')

        product = ContentType.objects.get(model=ct_model).model_class().objects.get(slug=slug)

        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, 
            cart=self.cart, 
            object_id=product.id, 
            content_type=ContentType.objects.get(model=ct_model)
        )

        if created:
            self.cart.products.add(cart_product)
        else:
            cart_product.quantity += 1
            cart_product.save()

        recalc_cart_fin_price(self.cart) # <=== recalculates final price and product quantity of a cart

        messages.add_message(request, messages.INFO, "Item successfuly added to your cart")

        return HttpResponseRedirect('/cart')


class ChangeQuantityView(CartMixin, View):
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('quantity'):
            ct_model = kwargs.get('ct_model') 
            slug = kwargs.get('slug')

            product = ContentType.objects.get(model=ct_model).model_class().objects.get(slug=slug)

            cart_product = CartProduct.objects.get(
                user=self.cart.owner, 
                cart=self.cart, 
                object_id=product.id, 
                content_type=ContentType.objects.get(model=ct_model)
            )

            cart_product.quantity = int(request.POST.get('quantity'))
            cart_product.save()

            recalc_cart_fin_price(self.cart)
            
            messages.add_message(request, messages.INFO, "Item's quantity changed")

        return HttpResponseRedirect('/cart')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model') 
        slug = kwargs.get('slug')

        product = ContentType.objects.get(model=ct_model).model_class().objects.get(slug=slug)

        cart_product = CartProduct.objects.get(
            user=self.cart.owner, 
            cart=self.cart, 
            object_id=product.id, 
            content_type=ContentType.objects.get(model=ct_model)
        )

        self.cart.products.remove(cart_product)
        cart_product.delete()

        recalc_cart_fin_price(self.cart)
        
        messages.add_message(request, messages.INFO, "Item successfuly removed from your cart")

        return HttpResponseRedirect('/cart')


class CheckoutView(CartMixin, View):
    
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories':  Category.objects.get_categories_for_left_sidebar(),
            'form': form
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.order_type = form.cleaned_data['order_type']
            new_order.delivery_date = form.cleaned_data['delivery_date']
            new_order.order_comment = form.cleaned_data['order_comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Thank you for your order! Our manager will contact you soon.')
            return HttpResponseRedirect('/')
        messages.add_message(request, messages.INFO, 'Failed to place your order, there must be something wrong with order data.')
        return HttpResponseRedirect('/checkout/')