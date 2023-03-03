from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                firstname = serializer.data['first_name']
                lastname = serializer.data['last_name']
                mobile = serializer.data['mobile']
                password = serializer.data['password']
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)
            try:
                user = User.objects.create_user(
                    first_name=firstname,
                    last_name=lastname,
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

        return Response(serializer.errors)
