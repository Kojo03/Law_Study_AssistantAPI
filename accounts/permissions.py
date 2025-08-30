from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Admin users can manage books and users"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

class IsAdminOrReadOnly(permissions.BasePermission):
    """Admin can modify, others can only read"""
    def has_permission(self, request, view):
        if request.method in permissions.READONLY_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

class IsLecturerOrAdmin(permissions.BasePermission):
    """Lecturers and admins can manage content"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
