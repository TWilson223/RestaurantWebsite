from django.urls import path
from LittleLemonAPI import views

urlpatterns = [
    path('groups/manager/users/', views.ManagerView.as_view()),
    path('groups/manager/users/<str:pk>', views.SingleManagerView.as_view()),
    path('groups/delivery-crew/users/', views.DeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<str:pk>', views.SingleDeliveryCrewView.as_view()),
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('category/', views.CategoriesView.as_view()),
    path('cart/menu-items/', views.CartView.as_view()),
    path('orders/', views.OrderView.as_view()),
    path('orders/<int:pk>', views.OrderItemView.as_view()),
]
