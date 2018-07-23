from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse = models.CharField(max_length=30, null=False, blank=False, default='Windsor')

    def __str__(self):
        return self.name+", "+self.warehouse


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100,validators=[MaxValueValidator(1000),MinValueValidator(0)])
    available = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def refill(self, prodname):
        product = Product.objects.get(name=prodname)
        product.stock = product.stock + 100
        product.save()
        return self.stock


class Client(User):
    PROVINCE_CHOICES = [
        ('AB', 'Alberta'),
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    ]

    company = models.CharField(max_length=50,  null=True, blank=True)
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)


class Order (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    num_units = models.PositiveIntegerField(default=0)
    order_status = [
        (0, 'Order Cancelled'),
        (1, 'Order Placed'),
        (2, 'Order Shipped'),
        (3, 'Order Delivered'),
    ]
    status_date = models.DateField

    def __str__(self):
        return str(self.client)

    def total_cost(self):
        return Product.price*int(self.num_units)




