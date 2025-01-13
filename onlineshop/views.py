from django.shortcuts import render

from .models import Order
from .serializers import OrderSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.core.mail import send_mail
from backend.settings import EMAIL_HOST_USER

from django.forms.models import model_to_dict

# Create your views here.
class OrderView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)

            return Response({
                'data': serializer.data,  # Corrected
                'message': "Orders Data fetched successfully"
            }, status=status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response({
                'data': [],
                'message': "Something went wrong while fetching"
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            incoming_data = request.data
            serializer = OrderSerializer(data = incoming_data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong"
                }, status=status.HTTP_400_BAD_REQUEST)

            subject = "New Order is Placed"
            message = "Dear Costumer " + incoming_data['customer_name'] + " Your order is placed now. Thanks for your order!"
            recipient_list = [incoming_data['customer_email']]
            print("sending email...")
            #send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': "Order created successfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': "Something went wrong while creating"
            }, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            incoming_data = request.data
            order_id = incoming_data.get('id')  # Corrected the method call
            print("Order id to be deleted:", order_id)

            if order_id is None:
                return Response({
                    'data': {},
                    'message': "Order id is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            order_to_be_updated = Order.objects.filter(id=order_id)
            print(type(order_to_be_updated))

            serializer = OrderSerializer(order_to_be_updated[0], data=incoming_data, partial=True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong"
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': "Order updated successfully"
            }, status=status.HTTP_200_OK)


        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': "Something went wrong while updating"
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.data
            order_id = data.get('id')  # Corrected the method call
            print("Order id to be deleted:", order_id)

            if order_id is None:
                return Response({
                    'data': {},
                    'message': "Order id is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            order_to_be_deleted = Order.objects.filter(id=order_id)

            if not order_to_be_deleted.exists():
                return Response({
                    'data': {},
                    'message': "Order not found with this id"
                }, status=status.HTTP_404_NOT_FOUND)
            #Print the record data before deletion
            order_data = order_to_be_deleted.first()
            print("Record Data:", model_to_dict(order_data))

            order_to_be_deleted[0].delete()

            return Response({
                'data': model_to_dict(order_data),
                'message': "Order deleted successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': "Something went wrong while deleting"
            }, status=status.HTTP_400_BAD_REQUEST)
