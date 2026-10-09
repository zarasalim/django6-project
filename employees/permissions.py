from rest_framework.permissions import BasePermission, SAFE_METHODS


def has_group(user, *group_names):
    return (
        user.is_authenticated
        and (
            user.is_superuser
            or user.groups.filter(name__in=group_names).exists()
        )
    )


class EmployeePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return has_group(request.user, 'Администратор')


class MoveEmployeePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return has_group(
            request.user,
            'Смотритель',
            'Администратор',
        )