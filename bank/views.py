from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from bank.models import TransactionDestinationUser
from bank.serializers import TransactionDestinationUserSerializer
from users.views import get_user


class CreateTransactionDestinationView(APIView):
    def post(self, request):
        serializer = TransactionDestinationUserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            destination_user = serializer.data['destination_user']
            card_number = serializer.data['card_number']

            if not user.account or not user.account.card:
                response = {'detail': 'User does not have account!'}
                return Response(response)

            try:
                transaction_destination = TransactionDestinationUser.objects.create(
                    user=user,
                    destination_name=destination_user,
                    card_number=card_number
                )
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            ser = TransactionDestinationUserSerializer(transaction_destination)
            return Response(ser.data)

        return Response(serializer.errors)

