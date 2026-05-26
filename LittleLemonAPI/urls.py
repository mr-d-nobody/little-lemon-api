from django.urls import path
from .views import CartView, DeliveryCrewView, ManagerUsersView, MenuItemsView, OrderView, SingleDeliveryCrewView, SingleManagerView, SingleMenuItemView, SingleOrderView

urlpatterns = [
     path(
        'menu-items',
        MenuItemsView.as_view()
    ),
     path(
    'menu-items/<int:pk>',
    SingleMenuItemView.as_view()
),
     path(
    'cart/menu-items',
    CartView.as_view()
),
     path(
        'orders',
        OrderView.as_view()
    ),
     
    path(
    'orders/<int:pk>',
    SingleOrderView.as_view()
    ),
    path(
    'groups/manager/users',
    ManagerUsersView.as_view()
),

path(
    'groups/manager/users/<int:pk>',
    SingleManagerView.as_view()
),

path(
    'groups/delivery-crew/users',
    DeliveryCrewView.as_view()
),

path(
    'groups/delivery-crew/users/<int:pk>',
    SingleDeliveryCrewView.as_view()
),
]
