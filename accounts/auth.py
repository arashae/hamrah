from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .models import Admin, Seller

def get_tokens_for_user(user, user_type):
    refresh = RefreshToken.for_user(user)
    refresh['user_type'] = user_type

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def authenticate_admin(username, password):
    try:
        admin = Admin.objects.get(username=username)
        if check_password(password, admin.password):
            return admin
    except Admin.DoesNotExist:
        return None

def authenticate_seller(username, password):
    try:
        seller = Seller.objects.get(username=username)
        if check_password(password, seller.password):
            return seller
    except Seller.DoesNotExist:
        return None 