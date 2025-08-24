from rest_framework import permissions

class IsLecturerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow lecturers or admins to access a view.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.role == 'lecturer' or request.user.role == 'admin')

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to access a view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'
