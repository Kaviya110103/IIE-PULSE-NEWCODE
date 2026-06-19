from rest_framework.permissions import BasePermission, IsAuthenticated


def is_admin_user(user):
    return bool(user and user.is_authenticated and (user.is_superuser or user.is_staff))


def is_staff_employee(user):
    if not user or not user.is_authenticated:
        return False
    if is_admin_user(user):
        return True
    from connect.models import Employee
    return Employee.objects.filter(user=user).exists()


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return is_admin_user(request.user)


class IsStaffEmployee(BasePermission):
    """Admin, Django staff, or linked Employee record."""

    def has_permission(self, request, view):
        return is_staff_employee(request.user)
