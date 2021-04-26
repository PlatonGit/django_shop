# Generated by Django 3.2 on 2021-04-23 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.PositiveIntegerField()),
                ('overall_price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Overall price')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Category name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('image', models.ImageField(upload_to='img/', verbose_name='Image')),
                ('description', models.TextField(null=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Price')),
                ('stock', models.IntegerField(verbose_name='In stock')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('status', models.CharField(choices=[('new', 'New'), ('in_process', 'In process'), ('completed', 'Completed')], default='new', max_length=150, verbose_name="Order's status")),
                ('order_type', models.CharField(choices=[('delivery', 'Delivery'), ('pickup', 'Pickup')], default='delivery', max_length=100, verbose_name="Order's type")),
                ('creation_date', models.DateTimeField(auto_now=True, verbose_name='Created at')),
                ('delivery_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Delivered at')),
                ('order_comment', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Order comment')),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.cart', verbose_name='Cart')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.customer', verbose_name='Customer')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name="Product's price")),
                ('cart_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.cart', verbose_name='Cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.product', verbose_name='Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Product in cart',
                'verbose_name_plural': 'Products in cart',
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.customer', verbose_name='Customer'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, to='web.CartProduct'),
        ),
    ]