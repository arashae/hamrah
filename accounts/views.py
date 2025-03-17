from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Admin, Customer, Seller
from .serializers import AdminSerializer, CustomerSerializer, SellerSerializer
from .permissions import IsAdmin, IsSeller, IsCustomer, IsOwnerOrAdmin
from .auth import authenticate_admin, authenticate_seller, get_tokens_for_user

# Create your views here.

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdmin]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        admin = authenticate_admin(username, password)
        if admin:
            tokens = get_tokens_for_user(admin, 'admin')
            return Response({
                'user': self.get_serializer(admin).data,
                'tokens': tokens
            })
        return Response({'error': 'نام کاربری یا رمز عبور اشتباه است'}, 
                      status=status.HTTP_400_BAD_REQUEST)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdmin|IsCustomer]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAdmin|IsSeller]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        seller = authenticate_seller(username, password)
        if seller:
            tokens = get_tokens_for_user(seller, 'seller')
            return Response({
                'user': self.get_serializer(seller).data,
                'tokens': tokens
            })
        return Response({'error': 'نام کاربری یا رمز عبور اشتباه است'}, 
                      status=status.HTTP_400_BAD_REQUEST)
