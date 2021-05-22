from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone 
from django.urls import reverse 

User = get_user_model()

def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})



class CategoryManager(models.Manager):
    
    CATEGORY_NAME_COUNT_NAME = {
        'Notebooks': 'notebook__count',
        'Smartphones': 'smartphone__count',
        'Smart TVs': 'smarttv__count',
        'Headphones': 'headphones__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_models_for_count(self, *model_names):
        return [models.Count(model_name) for model_name in model_names]

    def get_categories_for_left_sidebar(self):
        models = self.get_models_for_count('notebook', 'smartphone', 'smarttv', 'headphones')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data



class Category(models.Model):
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=250, unique=True, verbose_name='Category name')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})



class Product(models.Model):
    
    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)
    MAX_FILE_SIZE = 3145728
    
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

    def __str__(self):
        return self.title

    def get_url(self):
        return get_product_url(self, 'product_detail')

    def get_model_name(self):
        return self.__class__.__name__.lower()



class Notebook(Product):
    
    class Meta:
        verbose_name = 'Notebook'
        verbose_name_plural = 'Notebooks'

    display_type = models.CharField(max_length=250, verbose_name='Display type')
    processor_freq = models.CharField(max_length=250, verbose_name='Processor frequency')
    diagonal = models.CharField(max_length=250, verbose_name='Screen diagonal')
    
    video = models.CharField(max_length=250, verbose_name='Video card')
    ram = models.CharField(max_length=250, verbose_name='RAM')
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
    
    built_in_browser = models.BooleanField(default=False, verbose_name='Built-in browser')
    built_in_apps = models.CharField(max_length=250, verbose_name='Built-in apps', null=True, blank=True)



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

    connection_type = models.CharField(max_length=100, verbose_name='Headphones connection type', choices=CONNECTION_TYPE_CHOICES, default=CONNECTION_TYPE_WIRE)
    fastening = models.CharField(max_length=100, verbose_name='Headphones fastening', choices=FASTENING_CHOICES, default=FASTENING_EAR_BUDS)

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
    
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Overall price', default=0)

    def __str__(self):
        return 'Cart #%d' % self.id



class CartProduct(models.Model):

    class Meta:
        verbose_name = 'Product in cart'
        verbose_name_plural = 'Products in cart'

    user = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)

    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Final price', default=0)

    def __str__(self):
        return 'Product %s from cart #%d' % (self.content_object.title, self.cart.id)

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.content_object.price
        return super().save(*args, **kwargs) 



class Customer(models.Model):

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone number', null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Address', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='User\'s orders', related_name='orders', null=True, blank=True)

    def __str__(self):
        return 'Customer %s %s' % (self.user.first_name, self.user.last_name)



class Order(models.Model):

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    STATUS_DEFAULT = 'new'
    STATUS_IN_PROCESS = 'processing'
    STATUS_READY = 'ready'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = (
        (STATUS_DEFAULT, 'New'),
        (STATUS_IN_PROCESS, 'Order is in processing'),
        (STATUS_READY, 'Order is ready'),
        (STATUS_COMPLETED, 'Order completed')
    )

    TYPE_PICKUP = 'pickup'
    TYPE_DELIVERY = 'delivery'

    TYPE_CHOICES = (
        (TYPE_PICKUP, 'Pickup'),
        (TYPE_DELIVERY, 'Delivery')
    )


    customer = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, null=True, blank=True)
    
    first_name = models.CharField(max_length=255, verbose_name='Customer\'s first name')
    last_name = models.CharField(max_length=255, verbose_name='Customer\'s last name')
    phone = models.CharField(max_length=20, verbose_name='Phone number')
    address = models.CharField(max_length=1024, verbose_name='Address', null=True, blank=True)
    
    status = models.CharField(max_length=100, verbose_name='Order\'s status', choices=STATUS_CHOICES, default=STATUS_DEFAULT)
    order_type = models.CharField(max_length=100, verbose_name='Order\'s delivery method', choices=TYPE_CHOICES, default=TYPE_PICKUP)

    order_comment = models.TextField(max_length=1000, verbose_name='Order comment', null=True, blank=True)
    
    creation_date = models.DateTimeField(auto_now=True, verbose_name='Created at')
    delivery_date = models.DateTimeField(default=timezone.now, verbose_name='Will be delivered at')

    def __str__(self):
        return 'Order #%d' % self.id



class LatestProductManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        count = kwargs.get('count') # <--- updated here
        if count:           # <--- updated here
            count = [*count]        # <--- updated here
        else:                       # <--- updated here
            count = []              # <--- updated here

        products = list()

        ct_models = ContentType.objects.filter(model__in=args)
        count.extend([1 for i in range(len(ct_models) - len(count))]) # <--- updated here

        for i, ct_model in enumerate(ct_models): # <--- updated here
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:count[i]] # <--- updated here
            products.extend(model_products)
        
        if with_respect_to and with_respect_to in args:
            ct_models = ContentType.objects.filter(model=with_respect_to)
            if ct_models.exists():
                products = sorted(
                    products,
                    key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                )

        return products


        
class LatestProducts:
    objects = LatestProductManager()


# lt = LatestProducts()

# lt.objects.get_products_for_main_page('notebook', 'headphones', with_respect_to='headphones', count=(1, 1))





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

