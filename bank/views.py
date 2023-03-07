from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from bank.models import TransactionDestinationUser, TransactionType
from bank.serializers import TransactionDestinationUserSerializer, TransactionDestinationChangeValidationSerializer, \
    TransactionTypeSerializer
from users.views import get_user


class CreateTransactionDestinationView(APIView):
    def post(self, request):
        serializer = TransactionDestinationUserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            destination_user = serializer.data['destination_name']
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


class TransactionDestinationListAll(ListAPIView):
    queryset = TransactionDestinationUser.objects.all()
    serializer_class = TransactionDestinationUserSerializer


class TransactionDestinationList(ListAPIView):
    queryset = TransactionDestinationUser.objects.all()
    serializer_class = TransactionDestinationUserSerializer

    def get_queryset(self):
        user = get_user(self.request)
        return TransactionDestinationUser.objects.filter(user_id=user.id)


class TransactionDestinationDetailView(APIView):
    def get(self, request, pk):
        user = get_user(request)
        destination = TransactionDestinationUser.objects.filter(pk=pk, user_id=user.id).first()

        if not destination:
            response = {'detail': 'destination not found!'}
            return Response(response)

        serializer = TransactionDestinationUserSerializer(destination)
        return Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        user = get_user(request)
        destination = TransactionDestinationUser.objects.filter(pk=pk, user_id=user.id).first()

        if not destination:
            response = {'detail': 'destination not found!'}
            return Response(response)

        destination.delete()

        response = {'detail': 'destination deleted successfully!'}
        return Response(response)


class ChangeTransactionDestinationActivation(APIView):
    def post(self, request, pk):
        serializer = TransactionDestinationChangeValidationSerializer(request.data)
        user = get_user(request)
        destination = TransactionDestinationUser.objects.filter(pk=pk, user_id=user.id).first()

        if not destination:
            response = {'detail': 'destination not found!'}
            return Response(response)

        is_active = serializer.data['is_active']

        if is_active == 'True' or is_active == 'true':
            is_active = True
        elif is_active == 'False' or is_active == 'false':
            is_active = False

        destination.is_active = is_active
        destination.save()

        response = {'detail': f'destination activation is {is_active}!'}
        return Response(response)


class ChangeTransactionDestinationValidation(APIView):
    def post(self, request, pk):
        serializer = TransactionDestinationChangeValidationSerializer(request.data)
        user = get_user(request)
        destination = TransactionDestinationUser.objects.filter(pk=pk, user_id=user.id).first()

        if not destination:
            response = {'detail': 'destination not found!'}
            return Response(response)

        is_valid = serializer.data['is_valid']

        if is_valid == 'True' or is_valid == 'true':
            is_valid = True
        elif is_valid == 'False' or is_valid == 'false':
            is_valid = False

        destination.is_valid = is_valid
        destination.save()

        response = {'detail': f'destination activation is {is_valid}!'}
        return Response(response)


class CreateTransactionTypeView(APIView):
    def post(self, request):
        serializer = TransactionTypeSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data['title']
            tran_type = TransactionType.objects.filter(title=title).first()

            if not tran_type:
                response = {'detail': 'type not found!'}
                return Response(response)

            try:
                transaction_type = TransactionType.objects.create(title=title)
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            tran_serializer = TransactionTypeSerializer(transaction_type)
            return Response(tran_serializer.data)

        return Response(serializer.errors)
