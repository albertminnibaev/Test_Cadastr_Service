from rest_framework.permissions import BasePermission


# пользователь редактирует свой профиль
class IsProfileUser(BasePermission):
    message = "Вы не можете редактировать чужой профиль"

    def has_permission(self, request, view):
        return request.user == view.get_object()
