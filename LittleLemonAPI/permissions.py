from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class IsManager(BasePermission):
    def has_permission(self, request, view):
        isManager = request.user.groups.filter(name="Manager").exists()
        return bool(request.user and request.user.is_authenticated and isManager)

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        isDeliveryCrew = request.user.groups.filter(name="Delivery crew").exists()
        return bool(request.user and request.user.is_authenticated and isDeliveryCrew)
        
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        isDeliveryCrew = request.user.groups.filter(name="Delivery crew").exists()
        isManager = request.user.groups.filter(name="Manager").exists()
        return bool(request.user and request.user.is_authenticated and (isDeliveryCrew or isManager))

class IsStaff(BasePermission):
    def has_permission(self, request, view):        
        isManager = request.user.groups.filter(name="Manager").exists()
        return bool(request.user and request.user.is_authenticated and (IsAdminUser or isManager))

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        isCustomer = request.user.groups.filter(name="Customer").exists()
        return bool(request.user and request.user.is_authenticated and isCustomer)