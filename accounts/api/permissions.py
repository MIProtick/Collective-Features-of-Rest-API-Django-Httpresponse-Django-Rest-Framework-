from rest_framework import permissions

# class BlocklistPermission(permissions.BasePermission):
#     """
#     Global permission check for blocked IPs.
#     """

#     def has_permission(self, request, view):
#         ip_addr = request.META['REMOTE_ADDR']
#         blocked = Blocklist.objects.filter(ip_addr=ip_addr).exists()
#         return not blocked
        

class AnonymousPermission(permissions.BasePermission):
    """
    Global permission check for anynomous user.
    """
    message = 'You are already authenticated. Please logout and try again.'
    
    def has_permission(self, request, view):
        return request.user.is_anonymous

        
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'You are not authorized to manipulate this object.'
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
        

class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'You are not authorized to manipulate this object.'
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        
        # Instance must have an attribute named 
        return obj.owner == request.user
        

class IsOwnerOrSuperuser(permissions.BasePermission):
    """
    Object-level permission to only allow owners or super user of an object to access it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'You are not authorized to manipulate this object.'
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        
        # Instancownere must have an attribute named 
        return (obj.id == request.user.id or request.user.is_superuser)