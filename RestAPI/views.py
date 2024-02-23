from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import Group, User
from .serializers import UserSerializer, MenuItemSerializer, CartItemSerializer, OrderItemSerializer
from django.core.paginator import Paginator, EmptyPage
from .models import MenuItem, Cart, CartItem, Order, OrderItem


# Create your views here

class MenuItems(APIView):
    
    def get(self, request, item_id = None):
        if item_id is not None:
            return self.get_item(request, item_id)
        
        # menu_items = [
        #     {
        #         'name': 'Cheese Pizza',
        #         'price': 12.99,
                
        #     },
        #     {
        #         'name': 'Pepperoni Pizza',
        #         'price': 14.99
        #     },
        #     {
        #         'name': 'Meat Lovers Pizza',
        #         'price': 16.99
        #     }
        # ]
        menu_items = MenuItem.objects.select_related('category').all()
        # print(menu_items)
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        category = request.query_params.get('category')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default = 1)
        
        if to_price:
            # filtered_items = [item for item in menu_items if item['to_price'] <= float(price)]
            menu_items = menu_items.filter(price__lte = to_price)
            # return Response({'filtered_items': menu_items}, status=status.HTTP_200_OK)
        elif search:
            # search_items = list(filter(lambda item: search.lower() in item['name'].lower(), menu_items))
            # return Response({'search_items': search_items}, status=status.HTTP_200_OK)
            menu_items = menu_items.filter(title__startswith = search)
            
        elif category:
            menu_items = menu_items.filter(category__title = category)
        
        elif ordering:
            menu_items = menu_items.order_by(ordering)
        
        paginator = Paginator(menu_items, per_page=perpage)
        try:
            menu_items = paginator.page(number=page)
            # Serializar los datos paginados antes de devolver la respuesta
            # serialized_menu_items = [{'name': item['name'], 'price': item['price']} for item in menu_items_paginated]
            # return Response(serialized_menu_items, status=status.HTTP_200_OK)
        except EmptyPage:
            menu_items = []
        serialized_data = MenuItemSerializer(menu_items, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
        
    def get_item(self, request, item_id):
        menu_items = [
            {
                "id": 1,
                'name': 'Cheese Pizza',
                'price': 12.99
            },
            {
                "id": 2,
                'name': 'Pepperoni Pizza',
                'price': 14.99
            },
            {
                "id": 3,
                'name': 'Meat Lovers Pizza',
                'price': 16.99
            }
        ]
         
        munu_item = menu_items[int(item_id)]
        
        return Response(munu_item, status=status.HTTP_200_OK)
    
    @permission_classes([IsAuthenticated])
    def post(self, request, itemId = None):
        # Imprimir datos de la solicitud
        
        if itemId is not None:
            return self.post_item(request, itemId)
        
        print("Datos de la solicitud:")
        print(request.data)
        
        # Imprimir metadatos de la solicitud
        # print("Metadatos de la solicitud:")
        # print(request.META)
        
        # Obtener el usuario autenticado
        user = request.user
       
        # Obtener los grupos del usuario
        user_groups = user.groups.all()
    
        # Comprobar si el usuario está en un grupo específico
        if user_groups.filter(name='Manager').exists():
            #create new menu item
            menu_item = MenuItem(**request.data)
            menu_item.save()
            menu_item_serializer = MenuItemSerializer(menu_item)
            return Response({"Menu_item_added": menu_item_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
    @permission_classes([IsAuthenticated])
    def post_item(self, request, itemId):
        user = request.user
        # print("Usuario autenticado:")
        # print(user)
        user_groups = user.groups.all()
        if user_groups.filter(name='Manager').exists():
            # print("POST request with pk: " + str(pk))
            return Response({"message": "POST request with pk: " + str(itemId) +" is manager create item"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Unauthorized "}, status=status.HTTP_403_FORBIDDEN)
    
    @permission_classes([IsAuthenticated])
    def put(self, request, itemId):
        user = request.user
        print("Usuario autenticado:")
        print(user)
        user_groups = user.groups.all()
        if user_groups.filter(name='Manager').exists():
            print("POST request with itemId: " + str(itemId))
            return Response({"message": "POST request with itemId: " + str(itemId) +" is manager"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Unauthorized "}, status=status.HTTP_403_FORBIDDEN)
    
    @permission_classes([IsAuthenticated])
    def delete(self, request, itemId):
        try:
            user = request.user
            user_groups = user.groups.all()
            if user_groups.filter(name='Manager').exists():
                #logica para eliminar menu item
                print("POST request with itemId: " + str(itemId))
                return Response({"message": "POST request with itemId: " + str(itemId) +" is manager"}, status=status.HTTP_201_CREATED)
            return Response({"message": "Unauthorized "}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
    
class Manager(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        # Obtener todos los usuarios
        user = request.user
        if user.groups.filter(name='Manager').exists():
            # Obtener el grupo "Manager"
            # manager_group = Group.objects.get(name='Manager')

            # Obtener todos los usuarios que pertenecen al grupo "Manager"
            manager_users = User.objects.filter(groups__name='Manager')
            # print(list(manager_users))
            # serialized_users = UserSerializer(manager_users)
            serialized_users = [UserSerializer(user).data for user in manager_users]

            return Response(serialized_users, status=status.HTTP_200_OK)
        return Response({"message": "Unauthorized "}, status=status.HTTP_403_FORBIDDEN)
    
    @permission_classes([IsAuthenticated])
    def post(self, request, userId):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user_to_add = User.objects.get(pk=userId)
            manager_group = Group.objects.get(name='Manager')
            user_to_add.groups.add(manager_group)
            return Response({"message": "User added to Manager group" + str(user_to_add.username)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e) }, status=status.HTTP_404_NOT_FOUND)        
    
    @permission_classes([IsAuthenticated])
    def delete(sel, request, userId):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        user_to_delete = User.objects.get(pk=userId)
        try:
            #delete from group Delivery crew
            manager_group = Group.objects.get(name='Manager')
            user_to_delete.groups.remove(manager_group)
            return Response(status=status.HTTP_200_OK)
        except user_to_delete.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
class DeliveryCrew(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        users = User.objects.all()
        serialized_users = UserSerializer(users, many=True)
        return Response(serialized_users.data, status=status.HTTP_200_OK)
    
    def post(self, request, userId):
        
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user_to_add = User.objects.get(pk=userId)
            delivery_crew_group = Group.objects.get(name='Delivery crew')
            user_to_add.groups.add(delivery_crew_group)
            return Response({"message": "User added to Delivery Crew" + str(user_to_add.username)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(selft, request, userId):
        if not request.user.groups.filter(name='Manager').exists():
            return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        user_to_delete = User.objects.get(pk=userId)
        try:
            #delete from group Delivery crew
            delivery_crew_group = Group.objects.get(name='Delivery crew')
            user_to_delete.groups.remove(delivery_crew_group)
            return Response(status=status.HTTP_200_OK)
        except user_to_delete.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
             
class Cart(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # if not request.user:
        #     return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        
        cart_items = [
            {
                'id':1,
                'name': 'Cheese Pizza',
                'price': 12.99
            },
            {
                'id':2,
                'name': 'Pepperoni Pizza',
                'price': 14.99
            },
            {
                'id':3,
                'name': 'Meat Lovers Pizza',
                'price': 16.99
            }
        ]
        
        try:
            user = request.user
            # user_cart = user.cart
            serialize_user  = UserSerializer(user, many=False)
            return Response({'user': serialize_user.data, 'cart': cart_items}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        menu_item = request.data
        user_id = request.user.id
        #guardar en el modelo cart con el id del usuario actual
        return Response({"message": "Item added to cart"+ str(menu_item)}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, itemId = None):
        if itemId is not None:
            #eliminar item del carrito
            return self.delete_item(request, itemId)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    def delete_item(self, request, itemId):
        
        cart_items = [
            {
                'id':1,
                'name': 'Cheese Pizza',
                'price': 12.99
            },
            {
                'id':2,
                'name': 'Pepperoni Pizza',
                'price': 14.99
            },
            {
                'id':3,
                'name': 'Meat Lovers Pizza',
                'price': 16.99
            }
        ]
        
        new_cart_items = [item for item in cart_items if item['id'] != int(itemId)]
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class Order(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request, orderId = None):
        
        orders = [
            {
                'id': 1,
                'items': [
                    {
                        'name': 'Cheese Pizza',
                        'price': 12.99
                    },
                    {
                        'name': 'Pepperoni Pizza',
                        'price': 14.99
                    }
                ],
                'total': 27.98
            },
            {
                'id': 2,
                'items': [
                    {
                        'name': 'Meat Lovers Pizza',
                        'price': 16.99
                    }
                ],
                'total': 16.99
            }
        ]
        user = request.user
        user_groups = user.groups.all()
        if user_groups.filter(name='Delivery crew').exists():
            if orderId:
                return self.get_delivery(request, orderId)
            client_type = 'Delivery crew'
        elif user_groups.filter(name='Manager').exists():
            if orderId:
                return self.get_manager(request, orderId)
            client_type = f'Manager {user.username}'
        else:
            if orderId:
                return self.get_costumer(request, orderId)
            client_type = f'Customer {user.username}'

        return Response({'Orders': orders, 'Client': client_type}, status=status.HTTP_200_OK)
    
    def get_costumer(self, request, orderId):
        #logica para obtener una orden de un cliente
        orders = [
            {
                'id': 1,
                'items': [
                    {
                        'name': 'Cheese Pizza',
                        'price': 12.99
                    },
                    {
                        'name': 'Pepperoni Pizza',
                        'price': 14.99
                    }
                ],
                'total': 27.98
            },
            {
                'id': 2,
                'items': [
                    {
                        'name': 'Meat Lovers Pizza',
                        'price': 16.99
                    }
                ],
                'total': 16.99
            }
        ]
        order_to_return = orders[int(orderId)]
        return Response({"message": "Order for costumer", "order":order_to_return}, status=status.HTTP_200_OK)
    
    def get_manager(self, request, orderId):
        #logica para obtener una orden de un manager
        orders = [
            {
                'id': 1,
                'items': [
                    {
                        'name': 'Cheese Pizza',
                        'price': 12.99
                    },
                    {
                        'name': 'Pepperoni Pizza',
                        'price': 14.99
                    }
                ],
                'total': 27.98
            },
            {
                'id': 2,
                'items': [
                    {
                        'name': 'Meat Lovers Pizza',
                        'price': 16.99
                    }
                ],
                'total': 16.99
            }
        ]
        order_to_return = orders[int(orderId)]
        return Response({"message": "Order for manager"}, status=status.HTTP_200_OK)
    
    def get_delivery(self, request, orderId):
        #logica para obtener una orden de un repartidor
        orders = [
            {
                'id': 1,
                'items': [
                    {
                        'name': 'Cheese Pizza',
                        'price': 12.99
                    },
                    {
                        'name': 'Pepperoni Pizza',
                        'price': 14.99
                    }
                ],
                'total': 27.98
            },
            {
                'id': 2,
                'items': [
                    {
                        'name': 'Meat Lovers Pizza',
                        'price': 16.99
                    }
                ],
                'total': 16.99
            }
        ]
        order_to_return = orders[int(orderId)]
        return Response({"message": "Order for delivery crew"}, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user   
        #logica para crear una orden
        return Response({"message": "Order created for " + user.username}, status=status.HTTP_201_CREATED)
    
    def patch(self, request, orderId = None):
        user = request.user
        user_groups = user.groups.all()
        if user_groups.filter(name='Delivery crew').exists():
            return self.patch_delivery(request, orderId)
        elif user_groups.filter(name='Manager').exists():
            return self.patch_manger(request, orderId)
        else:
            return Response({"message": "Unauthorized "}, status=status.HTTP_403_FORBIDDEN)        
    
    def patch_manger(self, request, orderId):
        #logica para actualizar una orden de un manager
        #asignar delivery a la orden
        return Response({"message": "Order updated for manager"}, status=status.HTTP_200_OK)
    
    def patch_delivery(self, request, orderId):
        return Response({"message": "Order updated for delivery crew"}, status=status.HTTP_200_OK)
    
    def delete(self, request, orderId):
        user = request.user
        user_groups = user.groups.all()
        
        if user_groups.filter(name="Manager").exists():
            return Response({"message":'order deleted by manager'}, status=status.HTTP_200_OK)
        
        else:
            return Response({"message": "Unauthorized "}, status=status.HTTP_403_FORBIDDEN)        
             