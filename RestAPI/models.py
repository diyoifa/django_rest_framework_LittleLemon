from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    slug = models.SlugField(max_length=100)
    title = models.CharField(max_length=255, db_index=True)
    
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    feature = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_items = models.ManyToManyField(MenuItem, through='CartItem')
    total = models.DecimalField(max_digits=10, decimal_places=2)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('cart', 'menu_item')
        
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.PROTECT, related_name='delivery_crew')
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, db_index=True)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('order', 'menu_item')
    