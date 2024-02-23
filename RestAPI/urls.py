from django.urls import path
from . import views

urlpatterns = [
    path('menu-items/', views.MenuItems.as_view(), name='menuItems'),
    path('menu-items/<int:itemId>', views.MenuItems.as_view(), name='menuItems'),
    path('groups/manager/users', views.Manager.as_view(), name='get Managers'),
    path('groups/manager/users/<int:userId>', views.Manager.as_view(), name='Create manager'),
    path('groups/delivery-crew/users', views.DeliveryCrew.as_view(), name='all delivery crews'),
    path('groups/delivery-crew/users/<int:userId>', views.DeliveryCrew.as_view(), name='all delivery crews'),
    path('cart/menu-items', views.Cart.as_view(), name='get, delete or add  cart items'),
    path('cart/menu-items/<int:itemId>', views.Cart.as_view(), name='delete cart items'),
    path('orders', views.Order.as_view(), name='get all orders'),
    path('orders/<int:orderId>', views.Order.as_view(), name='get single orders'),
]
