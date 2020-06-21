from rest_framework.permissions import BasePermission


class IsAdvertOwner(BasePermission):
    
    def has_object_permission(self, request, view, obj):

        return request.user.store.advert == obj
