from urllib import request

from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.generics import DestroyAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, MenuItem, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer, UserSerializer
from .permissions import IsManagerOrReadOnly, IsManager, IsDeliveryCrew
# Create your views here.

class MenuItemsView(
    ListCreateAPIView
):

    queryset = MenuItem.objects.all()

    serializer_class = MenuItemSerializer

    permission_classes = [
        IsManagerOrReadOnly
    ]

    search_fields = ['title']

    ordering_fields = [
        'price',
        'inventory'
    ]

    filterset_fields = ['category', 'price']
    
    
class SingleMenuItemView(

    RetrieveUpdateDestroyAPIView

):

    queryset = MenuItem.objects.all()

    serializer_class = MenuItemSerializer

    permission_classes = [
        IsManagerOrReadOnly
    ]
    
class CartView(ListCreateAPIView):

    serializer_class = CartSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Cart.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):

        menuitem = MenuItem.objects.get(
            pk=self.request.data['menuitem']
        )

        quantity = int(
            self.request.data['quantity']
        )

        serializer.save(
            user=self.request.user,
            unit_price=menuitem.price,
            price=menuitem.price * quantity
        )

    def delete(self, request):

        Cart.objects.filter(
            user=request.user
        ).delete()

        return Response(
            {"message": "all cart items deleted"},
            status=status.HTTP_200_OK
        )
        
class OrderView(

    ListCreateAPIView

):

    serializer_class = OrderSerializer

    permission_classes = [
        IsAuthenticated
    ]

    search_fields = ['id']

    ordering_fields = ['date', 'total', 'status']

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):

        cart_items = Cart.objects.filter(
            user=request.user
        )
        if not cart_items.exists():
            return Response(
                {"message": "cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        total = sum(
            item.price for item in cart_items
        )
        order = Order.objects.create(
            user=request.user,
            total=total
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
        cart_items.delete()
        serializer = self.get_serializer(order)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    
class SingleOrderView(

    RetrieveUpdateDestroyAPIView

):

    queryset = Order.objects.all()

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):

        order = self.get_object()

        user = request.user
        if user.groups.filter(
            name='Manager'
        ).exists():

            delivery_crew_id = request.data.get(
                'delivery_crew'
            )

            status_value = request.data.get(
                'status'
            )

            if delivery_crew_id is not None:

                order.delivery_crew = User.objects.get(
                    pk=delivery_crew_id
                )

            if status_value is not None:

                order.status = status_value

            order.save()

            serializer = self.get_serializer(order)

            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.groups.filter(
            name='Delivery crew'
        ).exists():

            status_value = request.data.get(
                'status'
            )

            if status_value is not None:

                order.status = status_value

                order.save()

                serializer = self.get_serializer(order)

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:

                return Response(
                    {"message": "not authorized"},
                    status=status.HTTP_403_FORBIDDEN
                )
                
                
    def delete(self, request, *args, **kwargs):

        if request.user.groups.filter(
            name='Manager'
        ).exists():

            return super().delete(
                request,
                *args,
                **kwargs
            )

        return Response(
            {"message": "not authorized"},
            status=status.HTTP_403_FORBIDDEN
        )
        
class ManagerUsersView(

    ListCreateAPIView

):

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]

    serializer_class = UserSerializer
    
    def get_queryset(self):
        return User.objects.filter(groups__name='Manager')

    def post(self, request):

        user = User.objects.get(
            username=request.data['username']
        )

        manager_group = Group.objects.get(
            name='Manager'
        )

        manager_group.user_set.add(user)

        return Response(
            {"message": "user added to manager"},
            status=status.HTTP_201_CREATED
        )
        
class SingleManagerView(

    DestroyAPIView

):

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]
    
    def delete(self, request, pk):

        user = User.objects.get(pk=pk)

        manager_group = Group.objects.get(
            name='Manager'
        )

        manager_group.user_set.remove(user)

        return Response(
            {"message": "manager removed"},
            status=status.HTTP_200_OK
        )
        
class DeliveryCrewView(

    ListCreateAPIView

):

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(groups__name='Delivery crew')
    
    def post(self, request):

        user = User.objects.get(
            username=request.data['username']
        )

        crew_group = Group.objects.get(
            name='Delivery crew'
        )

        crew_group.user_set.add(user)

        return Response(
            {"message": "added to delivery crew"},
            status=status.HTTP_201_CREATED
        )
        
class SingleDeliveryCrewView(

    DestroyAPIView

):

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]
    
    def delete(self, request, pk):

        user = User.objects.get(pk=pk)

        crew_group = Group.objects.get(
            name='Delivery crew'
        )

        crew_group.user_set.remove(user)

        return Response(
            {"message": "removed from delivery crew"},
            status=status.HTTP_200_OK
        )