from rest_framework import permissions


class ProductPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allowing viewing for everyone - SAFE_METHODS = ('GET', 'OPTIONS', 'HEAD')
        if request.method in permissions.SAFE_METHODS:
            return True 
        # For user request like modifying, user must be is_staff
        if request.user and request.user.is_staff:
            return True
        # if modifying but not staff, then no permission
        return False
    
    
    
    
    
    
    

# class ProductPermissions(permissions.BasePermission):
#     # For list and retrieve (safe methods), allow everyone
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True  # Allow viewing for everyone
#         if request.user and request.user.is_staff:
#             return True  # Allow modifying for staff
#         return False
    
#     # Object-level permissions for update/delete actions
#     def has_object_permission(self, request, view, obj):
#         # Optionally, allow owners or specific roles to edit their own products
#         if request.user == obj.owner:
#             return True
#         return False
