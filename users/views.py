import datetime
import random

import jwt

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from users.permissions import IsAuthenticated, IsNotAuthenticated, IsAdmin
from users.models import User
from users.serializers import UserSerializer, ChangePasswordSerializer, ResetPasswordSerializer, UserMiniSerializer, \
    UserFullSerializer, UserActivationSerializer, UserApprovalSerializer


class RegisterView(APIView):
    permission_classes = (IsNotAuthenticated,)

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
    permission_classes = (IsNotAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'detail': 'Logged out successfully!'}


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = get_user(request)

        serializer = UserFullSerializer(user)
        return Response(serializer.data)


class UserListAllView(ListAPIView):
    permission_classes = (IsAdmin,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListActiveView(ListAPIView):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class UserListApprovedView(ListAPIView):
    permission_classes = (IsAdmin,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_approved=True)


class UserUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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


class ChangeUserApprovalView(APIView):
    permission_classes = (IsAdmin,)

    def post(self, request, pk):
        serializer = UserApprovalSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(pk=pk).first()
            is_approved = request.data['is_approved']

            if not user:
                response = {'detail': 'User NOT found!'}
                return Response(response)

            if is_approved == 'True' or is_approved == 'true':
                is_approved = True
            elif is_approved == 'False' or is_approved == 'false':
                is_approved = False

            user.is_approved = is_approved
            user.save()

            response = {'detail': f'User approval changed to {is_approved}!'}
            return Response(response)

        return Response(serializer.errors)


class ChangeUserActivationView(APIView):
    permission_classes = (IsAdmin,)

    def post(self, request, pk):
        serializer = UserActivationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(pk=pk).first()
            is_active = request.data['is_active']

            if not user:
                response = {'detail': 'User NOT found!'}
                return Response(response)

            if is_active == 'True' or is_active == 'true':
                is_active = True
            elif is_active == 'False' or is_active == 'false':
                is_active = False

            user.is_active = is_active
            user.save()

            response = {'detail': f'User approval changed to {is_active}!'}
            return Response(response)

        return Response(serializer.errors)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
