from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from bank.models import TransactionDestinationUser, TransactionType, TransactionWay
from bank.serializers import TransactionDestinationUserSerializer, TransactionDestinationChangeValidationSerializer, \
    TransactionTypeSerializer, TransactionTypeChangeActivationSerializer, TransactionWaySerializer
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

        is_active = request.data['is_active']

        if is_active == 'True' or is_active == 'true':
            is_active = True
        elif is_active == 'False' or is_active == 'false':
            is_active = False

        destination.is_active = is_active
        destination.save()

        response = {'detail': f'destination "{destination.destination_name}" activation is {is_active}!'}
        return Response(response)


class ChangeTransactionDestinationValidation(APIView):
    def post(self, request, pk):
        serializer = TransactionDestinationChangeValidationSerializer(request.data)
        user = get_user(request)
        destination = TransactionDestinationUser.objects.filter(pk=pk, user_id=user.id).first()

        if not destination:
            response = {'detail': 'destination not found!'}
            return Response(response)

        is_valid = request.data['is_valid']

        if is_valid == 'True' or is_valid == 'true':
            is_valid = True
        elif is_valid == 'False' or is_valid == 'false':
            is_valid = False

        destination.is_valid = is_valid
        destination.save()

        response = {'detail': f'destination "{destination.destination_name}" validation is {is_valid}!'}
        return Response(response)


class CreateTransactionTypeView(APIView):
    def post(self, request):
        serializer = TransactionTypeSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data['title']
            tran_type = TransactionType.objects.filter(title=title).exists()

            if tran_type:
                response = {'detail': 'type already exist!'}
                return Response(response)

            try:
                transaction_type = TransactionType.objects.create(title=title)
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            tran_serializer = TransactionTypeSerializer(transaction_type)
            return Response(tran_serializer.data)

        return Response(serializer.errors)


class TransactionTypeListView(ListAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer

    def get_queryset(self):
        return TransactionType.objects.filter(is_active=True)


class TransactionDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionTypeSerializer
    queryset = TransactionType.objects.all()

    def update(self, request, *args, **kwargs):
        tran_type = TransactionType.objects.filter(pk=kwargs.get('pk')).first()
        title = request.data['title']

        if not tran_type:
            response = {'detail': 'type not found!'}
            return Response(response)

        tran_type.title = title
        tran_type.save()

        serializer = TransactionTypeSerializer(tran_type)
        return Response(serializer.data)


class ChangeTransactionTypeActivation(APIView):
    def post(self, request, pk):
        serializer = TransactionTypeChangeActivationSerializer(data=request.data)
        if serializer.is_valid():
            tran_type = TransactionType.objects.filter(pk=pk).first()
            is_active = serializer.data['is_active']

            if not tran_type:
                response = {'detail': 'type not found!'}
                return Response(response)

            if is_active == 'True' or is_active == 'true':
                is_active = True
            elif is_active == 'False' or is_active == 'false':
                is_active = False

            tran_type.is_active = is_active
            tran_type.save()

            response = {'detail': f'type activation "{tran_type.title}" changed into {is_active}!'}
            return Response(response)

        return Response(serializer.errors)


class CreateTransactionWayView(APIView):
    def post(self, request):
        serializer = TransactionWaySerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data['title']
            tran_way = TransactionWay.objects.filter(title=title).exists()

            if tran_way:
                response = {'detail': 'transaction way already exist!'}
                return Response(response)

            try:
                transaction_way = TransactionWay.objects.create(title=title)
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            tran_serializer = TransactionWaySerializer(transaction_way)
            return Response(tran_serializer.data)

        return Response(serializer.errors)
