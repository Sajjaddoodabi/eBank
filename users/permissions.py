import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import User


def get_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()

    return user


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return bool(user and user.is_authenticated)


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return user.is_anonymous


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return bool(user and user.is_staff)


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return bool(user and user.is_staff and user.is_superuser)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = get_user(request)
        if request.method in SAFE_METHODS:
            return True
        return bool(user and user.is_staff)
