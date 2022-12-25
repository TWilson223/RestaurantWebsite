from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from django.contrib.auth.models import User, Group
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from LittleLemonAPI.models import *
from LittleLemonAPI.serializers import *
from LittleLemonAPI import permissions

class ManagerView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsStaff]

        return [permission() for permission in permission_classes]  

class SingleManagerView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsStaff]

        return [permission() for permission in permission_classes]  

class DeliveryCrewView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Delivery crew")
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsStaff]

        return [permission() for permission in permission_classes]  

class SingleDeliveryCrewView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Delivery crew")
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = [permissions.IsStaff]

        return [permission() for permission in permission_classes]  

class MenuItemsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = GetMenuItemSerializer

    def post(self, request: HttpRequest) -> HttpResponse:
        if(request.user.groups.filter(name="Manager").exists()):
            serializer = SaveMenuItemSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error":"Access Denied. You do not have the correct permissions."}, status=status.HTTP_403_FORBIDDEN)

    ordering_fields = ['price']
    filterset_fields = ['price']
    search_fields = ['title', 'category__title']

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = GetMenuItemSerializer

    def get_permissions(self):
        permission_classes = []

        if self.request.method != 'GET':
            permission_classes = [permissions.IsManager]

        return [permission() for permission in permission_classes]   

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_permissions(self):
        permission_classes = []

        if self.request.method != 'GET':
            permission_classes = [permissions.IsCustomer]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        items = Cart.objects.filter(user=self.request.user)
        if items.count() > 0:
           items.delete()
           return Response(status=status.HTTP_204_NO_CONTENT)
           
        return Response(status=status.HTTP_400_BAD_REQUEST)

class OrderView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.groups.count()==0: #normal customer - no group
            return Order.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='Delivery Crew').exists(): #delivery crew
            return Order.objects.all().filter(delivery_crew=self.request.user)  #only show oreders assigned to him
        else: #delivery crew or manager
            return Order.objects.all()
        # else:
        #     return Order.objects.all()

    def create(self, request, *args, **kwargs):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message:": "no item in cart"})

        data = request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
        if (order_serializer.is_valid()):
            order = order_serializer.save()

            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = OrderItem(
                    order=order,
                    menuitem_id=item['menuitem_id'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
                orderitem.save()

            Cart.objects.all().filter(user=self.request.user).delete() #Delete cart items

            result = order_serializer.data.copy()
            result['total'] = total
            return Response(order_serializer.data)
    
    def get_total_price(self, user):
        total = 0
        items = Cart.objects.all().filter(user=user).all()
        for item in items.values():
            total += item['price']
        return total

    ordering_fields = ['total', 'date']
    filterset_fields = ['total','date']
    search_fields = ['user']
    
class OrderItemView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        permission_classes = []

        if self.request.method == 'DELETE':
            permission_classes = [permissions.IsManager]
        elif self.request.method != 'GET':
            permission_classes = [permissions.IsStaff]

        return [permission() for permission in permission_classes]

class CategoriesView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'POST':
            if request.user.groups.filter(name='Manager').exists():
                serialized_item = CategorySerializer(data=request.data)
                serialized_item.is_valid(raise_exception=True)
                serialized_item.save()
                return Response(serialized_item.validated_data, status.HTTP_201_CREATED)
            else:
                return Response({"message": "Access Denied. You do not have the correct permissions."}, status.HTTP_403_FORBIDDEN)
