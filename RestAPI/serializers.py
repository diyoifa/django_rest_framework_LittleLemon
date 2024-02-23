from rest_framework import serializers
from django.contrib.auth.models import  User
from .models import Category, MenuItem, Cart, CartItem, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, source='category')
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'feature', 'category', 'category_id']
        
class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'menu_item', 'quantity', 'unit_price', 'price']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, source='cartitem_set')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items']
        
class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'quantity', 'unit_price', 'price']

