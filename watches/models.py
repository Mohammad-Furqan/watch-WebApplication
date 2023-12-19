from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
# watches/models.py

class Watch(models.Model):  
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='watch_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0)

    def is_in_stock(self, quantity=1):
        return self.stock_quantity >= quantity

    def decrease_stock(self, quantity):
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
            return True
        return False

    def increase_stock(self, quantity):
        self.stock_quantity += quantity
        self.save()

    def __str__(self):
        return self.name



class Order(models.Model):
    PENDING = 'pending'
    PROCESSING = 'processing'
    SHIPPING = 'shipping'
    DELIVERED = 'delivered'
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPING, 'Shipping'), 
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Watch', through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    payment_successful = models.BooleanField(default=False)
    order_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
 
    def get_status_display(self):
        try:
            return dict(self.STATUS_CHOICES)[self.status]
        except KeyError:
            return "Unknown Status"

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    watch = models.ForeignKey('Watch', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)





class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('Watch', through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    watch = models.ForeignKey('Watch', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

