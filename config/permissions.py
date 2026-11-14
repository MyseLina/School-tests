from rest_framework.permissions import BasePermission, SAFE_METHODS

def is_admin(user):
    return user.is_staff or user.is_superuser

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        m = request.user
        return m.is_authenticated and hasattr(m, 'students')

class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        m = request.user
        return m.is_authenticated and (hasattr(m, 'teachers') or is_admin(m))

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        m = request.user
        if not m.is_authenticated:
            return False
        return request.method in SAFE_METHODS or is_admin(m)