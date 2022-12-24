from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import User, Group
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework import status
from LittleLemonAPI.models import *
from LittleLemonAPI.serializers import *

@permission_classes([IsAdminUser])
class ManagerView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = UserSerializer

@permission_classes([IsAdminUser])
class SingleManagerView(generics.RetrieveDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = UserSerializer

@permission_classes([IsAdminUser])
class DeliveryCrewView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Delivery crew")
    serializer_class = UserSerializer

@permission_classes([IsAdminUser])
class SingleDeliveryCrewView(generics.RetrieveDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name="Delivery crew")
    serializer_class = UserSerializer

@permission_classes([IsAuthenticated])
class MenuItemsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []

        if self.request.method != 'GET':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    ordering_fields = ['price']
    filterset_fields = ['price']
    search_fields = ['title']

@permission_classes([IsAuthenticated])
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []

        if self.request.method != 'GET':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

@permission_classes([IsAuthenticated])
class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        items = Cart.objects.filter(user=self.request.user)
        if items.count() > 0:
           items.delete()
           return Response(status=status.HTTP_204_NO_CONTENT)
           
        return Response(status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class OrderView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    ordering_fields = ['total', 'date']
    filterset_fields = ['total','date']
    search_fields = ['user']
    

@permission_classes([IsAuthenticated])
class OrderItemView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all().filter(user=self.request.user)

    def get_permissions(self):
        permission_classes = []

        if self.request.method == 'DELETE':
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]


@permission_classes([IsAuthenticated])
class CategoriesView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
