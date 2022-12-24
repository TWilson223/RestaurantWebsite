from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User, Group

class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email','groups']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']

        extra_kwargs = {
            'price' : {'min_value' : 2}
        }

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id','user','menuitem','quantity','unit_price','price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','user','delivery_crew','status','total','date']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','order','menuitem','quantity','unit_price','price']