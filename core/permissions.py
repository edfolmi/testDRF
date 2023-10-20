from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        #SAFE_METHODS means ['GET', 'HEAD', 'OPTIONS'] as readonly
        if request.method in permissions.SAFE_METHODS:
            return True

        #Means allow PUT, PATCH, DELETE by the owner of post.
        return obj.creator == request.user