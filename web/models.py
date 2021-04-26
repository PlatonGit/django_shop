from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
 
User = get_user_model()


class Category(models.Model):
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=250, unique=True, verbose_name='Category name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    
    class Meta:
        abstract = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Title')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')
    image = models.ImageField(verbose_name='Image') # , upload_to='img/'
    # stock = models.IntegerField(verbose_name='In stock')

    def __str__(self):
        return self.title


class Notebook(Product):
    
    class Meta:
        verbose_name = 'Notebook'
        verbose_name_plural = 'Notebooks'

    display_type = models.CharField(max_length=250, verbose_name='Display type')
    processor_freq = models.CharField(max_length=250, verbose_name='Processor frequency')
    diagonal = models.CharField(max_length=250, verbose_name='Screen diagonal')
    
    video = models.CharField(max_length=250, verbose_name='Video card')
    ram = models.CharField(max_length=250, verbose_name='Random-access memory')
    os = models.CharField(max_length=250, verbose_name='Operating system')
    
    battery = models.CharField(max_length=250, verbose_name= 'Battery life')


class Smartphone(Product):
    
    class Meta:
        verbose_name = 'Smartphone'
        verbose_name_plural = 'Smartphones'

    diagonal = models.CharField(max_length=250, verbose_name='Screen diagonal')
    display_type = models.CharField(max_length=250, verbose_name='Display type')
    resolution = models.CharField(max_length=250, verbose_name='Screen resolution')
    
    ram = models.CharField(max_length=250, verbose_name='Operative Memory')
    sd = models.BooleanField(default=False, verbose_name='SD card')
    sd_volume = models.CharField(max_length=250, verbose_name='Maximal SD volume', null=True, blank=True)
    
    battery = models.CharField(max_length=250, verbose_name='Battery life')

    main_cam = models.CharField(max_length=250, verbose_name='Main camera')
    frontal_cam = models.CharField(max_length=250, verbose_name='Frontal camera')


class SmartTV(Product):
    
    class Meta:
        verbose_name = 'Smart TV'
        verbose_name_plural = 'Smart TVs'

    diagonal = models.CharField(max_length=250, verbose_name='Screen diagonal')
    resolution = models.CharField(max_length=250, verbose_name='Screen resolution')
    
    built_in_browser = models.CharField(max_length=250, verbose_name='Built-in web browser', null=True, blank=True)
    built_in_apps = models.CharField(max_length=250, verbose_name='Bulit-in apps', null=True, blank=True)


class Headphones(Product):
    
    class Meta:
        verbose_name = 'Headphones'
        verbose_name_plural = 'Headphones'

    CONNECTION_TYPE_WIRE = 'wire'
    CONNECTION_TYPE_WIRELESS = 'wireless'
    
    CONNECTION_TYPE_CHOICES = (
        (CONNECTION_TYPE_WIRE, 'By wire / MiniJack'),
        (CONNECTION_TYPE_WIRELESS, 'Wireless connection / Bluetooth')
    )

    FASTENING_EAR_BUDS = 'earbuds'
    FASTENING_VERTICAL_BOW = 'vertical_bow'

    FASTENING_CHOICES = (
        (FASTENING_EAR_BUDS, 'Ear buds'),
        (FASTENING_VERTICAL_BOW, 'Vertical bow')
    )

    connection_type = models.CharField(max_length=100, verbose_name='Headphone connection type', choices=CONNECTION_TYPE_CHOICES, default=CONNECTION_TYPE_WIRE)
    fastening = models.CharField(max_length=100, verbose_name='Headphone fastening', choices=FASTENING_CHOICES, default=FASTENING_EAR_BUDS)

    speaker_freq = models.CharField(max_length=250, verbose_name='Speaker frequency')
    battery = models.CharField(max_length=250, verbose_name='Battery life', null=True, blank=True)
    


class Cart(models.Model):

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    owner = models.ForeignKey('Customer', verbose_name='Cart owner', on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField('CartProduct', blank=True, related_name='products')
    total_products = models.PositiveIntegerField(default=0)
    
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)
    
    overall_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Overall price', default=0)

    def __str__(self):
        return 'Cart #%d' % self.id


class CartProduct(models.Model):

    class Meta:
        verbose_name = 'Product in cart'
        verbose_name_plural = 'Products in cart'

    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart_fk = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)

    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Final price', default=0)

    def __str__(self):
        return 'Product %s from cart #%d' % (self.content_object.title, self.cart.id)


class Customer(models.Model):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone number', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='User\'s orders', related_name='orders', null=True, blank=True)

    def __str__(self):
        return 'Customer %s %s' % (self.user.first_name, self.user.last_name)


class Order(models.Model):

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    customer = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=255, verbose_name='Customer\'s first name')
    last_name = models.CharField(max_length=255, verbose_name='Customer\'s last name')
    phone = models.CharField(max_length=20, verbose_name='Phone number', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Address', null=True, blank=True)

    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, null=True, blank=True)

    STATUS_DEFAULT = 'new'
    STATUS_IN_PROCESS = 'processing'
    STATUS_READY = 'ready'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = (
        (STATUS_DEFAULT, 'New'),
        (STATUS_IN_PROCESS, 'Processing'),
        (STATUS_READY, 'Ready'),
        (STATUS_COMPLETED, 'Completed')
    )

    TYPE_PICKUP = 'pickup'
    TYPE_DELIVERY = 'delivery'

    TYPE_CHOICES = (
        (TYPE_PICKUP, 'Pickup'),
        (TYPE_DELIVERY, 'Delivery')
    )

    status = models.CharField(max_length=100, verbose_name='Order\'s status', choices=STATUS_CHOICES, default=STATUS_DEFAULT)
    order_type = models.CharField(max_length=100, verbose_name='Order\'s type', choices=TYPE_CHOICES, default=TYPE_PICKUP)
    
    creation_date = models.DateTimeField(auto_now=True, verbose_name='Created at')
    delivery_date = models.DateTimeField(default=timezone.now, verbose_name='Delivered at')

    order_comment = models.TextField(max_length=1000, verbose_name='Order comment', null=True, blank=True)


    def __str__(self):
        return 'Order #%d' % self.id





# # GENERAL PRODUCT CATEGORIES:


# # NOTEBOOK///////////////////////////////////////////////////////////////
# class Notebook(AbstractProduct):
#     # Notebook characteristics:
#     ram_characteristics = models.PositiveIntegerField(verbose_name='RAM')
#     screen_size = models

# # NOTEBOOK SUBCATEGORIES:
# class GamingNotebook(Notebook):
#     # Gaming notebook characteristics:
#     pass


# class BusinessNotebook(Notebook):
#     # Business notebook characteristics:
#     pass


# class OfficeNotebook(Notebook):
#     # Office notebook characteristics:
#     pass



# # SMARTPHONE///////////////////////////////////////////////////////////////
# class Smartphone(AbstractProduct):
#     # Smartphone characteristics:
#     pass















# Category
# Product

# Cart
# CartProduct (-> Customer)

# Customer (fk -> User)

# Order


# 1
# Specification
# (ContentType)

# 2
# Abstract Product



# Create your models here.

