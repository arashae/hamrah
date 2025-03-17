from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return hasattr(request.user, 'admin')
        except:
            return False

class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return hasattr(request.user, 'seller')
        except:
            return False

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        try:
            return hasattr(request.user, 'customer')
        except:
            return False

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'admin'):
            return True
        return obj.id == request.user.id 