import datetime

import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        try:
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

        if not user:
            raise AuthenticationFailed('Unauthenticated')

        serializer = UserSerializer(user)
        return Response(serializer.data)


def get_user(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')

    user = User.objects.filter(id=payload['id']).first()

    return user


class ApproveUser(APIView):
    def post(self, request):
        pass


class ActiveUser(APIView):
    def post(self, request):
        pass
