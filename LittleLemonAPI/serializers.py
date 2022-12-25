from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User, Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email','groups']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug','title']

class GetMenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']

        extra_kwargs = {
            'price' : {'min_value' : 2}
        }

class SaveMenuItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MenuItem
        fields = ['title', 'price', "featured", 'category']  

class UpdateMenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuItem
        fields = ['title', 'price', "featured", 'category']
        extra_kwargs = {
            "title": {'required':False},
            "price": {'required':False},
            "featured": {'required':False},
            "category": {'required':False},
        }

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )


    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs

    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }

class GetOrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    menuitems = serializers.SerializerMethodField(method_name="get_menuItems")
    class Meta:
        model = Order
        fields = "__all__"
        

    def get_menuItems(self, obj):
        order_items = models.OrderItem.objects.filter(order = obj)
        return order_items.values()

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):

    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew',
                  'status', 'date', 'total', 'orderitem']