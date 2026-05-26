from rest_framework import serializers
from .models import Cart, MenuItem, Category, Order, OrderItem
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = ['id', 'title', 'slug']

class MenuItemSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)

    category_id = serializers.IntegerField(write_only=True)

    class Meta:

        model = MenuItem

        fields = [
            'id',
            'title',
            'price',
            'inventory',
            'category',
            'category_id'
        ]
        
class CartSerializer(serializers.ModelSerializer):

    class Meta:

        model = Cart

        fields = [
            'id',
            'menuitem',
            'quantity',
            'unit_price',
            'price'
        ]
        
class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = OrderItem

        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):

    orderitems = OrderItemSerializer(
        many=True,
        read_only=True,
        source='orderitem_set'
    )

    class Meta:

        model = Order

        fields = [
            'id',
            'user',
            'delivery_crew',
            'status',
            'total',
            'date',
            'orderitems'
        ]