import datetime
import random

import jwt

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from users.models import User
from users.serializers import UserSerializer, ChangePasswordSerializer, ResetPasswordSerializer, UserMiniSerializer, \
    UserFullSerializer


class RegisterView(APIView):
    def post(self, request):
        try:
            birth_date = request.data['birth_date']
            firstname = request.data['first_name']
            lastname = request.data['last_name']
            mobile = request.data['mobile']
            username = request.data['username']
            password = request.data['password']
        except Exception as e:
            response = {'detail': str(e)}
            return Response(response)
        try:
            user = User.objects.create_user(
                birth_date=birth_date,
                first_name=firstname,
                last_name=lastname,
                username=username,
                mobile=mobile,
            )
            user.set_password(password)
            user.save()

        except Exception as e:
            response = {'detail': str(e)}
            return Response(response)
        else:
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = User.objects.filter(username=username).first()

        if not user:
            response = {'detail': 'User NOT found!'}
            return Response(response)

        if not user.check_password(password):
            response = {'detail': 'User NOT found!'}
            return Response(response)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {'jwt': token}
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'detail': 'Logged out successfully!'}


class UserView(APIView):
    def get(self, request):
        user = get_user(request)

        serializer = UserFullSerializer(user)
        return Response(serializer.data)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(APIView):
    def put(self, request):
        user = get_user(request)

        user.first_name = request.data['first_name']
        user.last_name = request.data['last_name']
        user.username = request.data['username']
        user.mobile = request.data['mobile']
        user.national_code = request.data['national_code']
        user.postal_code = request.data['postal_code']
        user.address = request.data['address']

        user.save()

        user_ser = UserFullSerializer(user)
        return Response(user_ser.data)


def patch(self, request):
    serializer = UserMiniSerializer(data=request.data)
    if serializer.is_valid():
        pass
    return Response()


class UserDeleteView(APIView):
    def delete(self, request):
        user = get_user(request)
        user.delete()

        response = {'detail': 'User deleted successfully!'}
        return Response(response)


def get_user(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')

    user = User.objects.filter(id=payload['id']).first()

    if not user:
        raise AuthenticationFailed('Unauthenticated')

    return user


class ApproveUser(APIView):
    def post(self, request):
        user = get_user(request)

        user.is_approved = True
        user.save()

        response = {'detail': 'User has been approved!'}
        return Response(response)


class ActiveUser(APIView):
    def post(self, request):
        user = get_user(request)

        user.is_active = True
        user.save()

        response = {'detail': 'User has been activated!'}
        return Response(response)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)

            password = request.data['current_password']
            new_password = request.data['new_password']
            confirm_password = request.data['confirm_password']

            if not user.check_password(password):
                response = {'detail': 'current password is wrong!'}
                return Response(response)

            if new_password != confirm_password:
                response = {'detail': 'passwords do NOT match'}
                return Response(response)

            user.set_password(confirm_password)
            user.save()

            response = {'detail': 'password changed successfully!'}
            return Response(response)

        return Response(serializer.errors)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            user.is_active = False
            user.save()

            confirm_code = request.data['confirm_code']
            if confirm_code != '12345':
                response = {'detail': 'code is invalid!'}
                return Response(response)

            password = random.randint(a=10000, b=100000)
            user.set_password(str(password))
            user.save()

            response = {'detail': f'password set to {password} !'}
            return Response(response)

        return Response(serializer.errors)
