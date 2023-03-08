import datetime
import random

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, DestroyAPIView

from bank.models import TransactionDestinationUser, TransactionType, TransactionWay, Transaction
from bank.serializers import TransactionDestinationUserSerializer, TransactionDestinationChangeValidationSerializer, \
    TransactionTypeSerializer, TransactionTypeChangeActivationSerializer, TransactionWaySerializer, \
    TransactionSerializer
from bank_account.models import Account
from users.views import get_user


class CreateTransactionView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            destination = request.data['transaction_to']
            des_type = request.data['type']
            amount = int(request.data['amount'])

            account = Account.objects.filter(user_id=user.id).first()

            destination_user = TransactionDestinationUser.objects.filter(card_number=destination,
                                                                         user_id=user.id).first()
            destination_type = TransactionType.objects.filter(title=des_type).first()

            if not account:
                response = {'detail': 'user does NOT have an account!'}
                return Response(response)

            if not destination_user:
                response = {'detail': 'destination user is invalid!'}
                return Response(response)

            if not destination_type:
                response = {'detail': 'destination type is invalid!'}
                return Response(response)

            if destination_type.title != 'charge':
                if amount > account.balance:
                    response = {'detail': 'Not enough balance!'}
                    return Response(response)

            reference_number = random.randint(10 ** 10, 10 ** 11)

            try:
                transaction = Transaction.objects.create(
                    user_id=user.id,
                    transaction_to=destination_user,
                    type=destination_type,
                    amount=amount,
                    reference_number=reference_number
                )
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            transaction_ser = TransactionSerializer(transaction)
            return Response(transaction_ser.data)

        return Response(serializer.errors)


class DoneTransactionView(APIView):
    def post(self, request, pk):
        user = get_user(request)
        transaction = Transaction.objects.filter(pk=pk, is_done=False, is_fail=False).first()
        account = Account.objects.filter(user_id=user.id).first()

        if not transaction:
            response = {'detail': 'transaction NOT found!'}
            return Response(response)

        if not account:
            response = {'detail': 'account NOT found!'}
            return Response(response)

        transaction.is_done = True
        transaction.save()

        if transaction.type.title == 'charge':
            account.balance += transaction.amount
            account.save()

        transaction_serializer = TransactionSerializer(transaction)
        return Response(transaction_serializer.data)


class FailTransactionView(APIView):
    def post(self, request, pk):
        user = get_user(request)
        transaction = Transaction.objects.filter(pk=pk, is_done=False, is_fail=False).first()
        account = Account.objects.filter(user_id=user.id).first()

        if not transaction:
            response = {'detail': 'transaction NOT found!'}
            return Response(response)

        if not account:
            response = {'detail': 'account NOT found!'}
            return Response(response)

        transaction.is_done = False
        transaction.save()

        transaction_serializer = TransactionSerializer(transaction)
        return Response(transaction_serializer.data)


class TransactionDetailView(APIView):
    def get(self, request, pk):
        transaction = Transaction.objects.filter(pk=pk).first()

        if not transaction:
            response = {'detail': 'transaction NOT found!'}
            return Response(response)

        transaction_serializer = TransactionSerializer(transaction)
        return Response(transaction_serializer.data)


class TransactionAllListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDoneListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(is_done=True, is_fail=False)


class TransactionFailListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(is_done=False, is_fail=True)


class TransactionQueueListView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(is_done=False, is_fail=False)


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


class TransactionDestinationListAllView(ListAPIView):
    queryset = TransactionDestinationUser.objects.all()
    serializer_class = TransactionDestinationUserSerializer


class TransactionDestinationAllListView(ListAPIView):
    queryset = TransactionDestinationUser.objects.all()
    serializer_class = TransactionDestinationUserSerializer


class TransactionDestinationActiveListView(ListAPIView):
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


class ChangeTransactionDestinationActivationView(APIView):
    def post(self, request, pk):
        serializer = TransactionDestinationChangeValidationSerializer(request.data)
        if serializer.is_valid():
            destination = TransactionDestinationUser.objects.filter(pk=pk).first()

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

            response = {'detail': f'destination "{destination.destination_name}" activation is {is_active}!'}
            return Response(response)

        return Response(serializer.errors)


class ChangeTransactionDestinationValidationView(APIView):
    def post(self, request, pk):
        serializer = TransactionDestinationChangeValidationSerializer(data=request.data)
        if serializer.is_valid():
            destination = TransactionDestinationUser.objects.filter(pk=pk).first()

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

            response = {'detail': f'destination "{destination.destination_name}" validation is {is_valid}!'}
            return Response(response)
        return Response(serializer.errors)


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


class TransactionTypeListAllView(ListAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer


class TransactionTypeListActiveView(ListAPIView):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer

    def get_queryset(self):
        return TransactionType.objects.filter(is_active=True)


class TransactionTypeDetailView(RetrieveUpdateDestroyAPIView):
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


class ChangeTransactionTypeActivationView(APIView):
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


class TransactionWayDetailView(RetrieveUpdateDestroyAPIView):
    queryset = TransactionWay.objects.all()
    serializer_class = TransactionWaySerializer

    def update(self, request, *args, **kwargs):
        tran_way = TransactionWay.objects.filter(pk=kwargs.get('pk')).first()
        title = request.data['title']

        if not tran_way:
            response = {'detail': 'type not found!'}
            return Response(response)

        tran_way.title = title
        tran_way.save()

        serializer = TransactionWaySerializer(tran_way)
        return Response(serializer.data)


class TransactionWayAllListView(ListAPIView):
    serializer_class = TransactionWaySerializer
    queryset = TransactionWay.objects.all()


class TransactionWayActiveListView(ListAPIView):
    serializer_class = TransactionWaySerializer
    queryset = TransactionWay.objects.all()

    def get_queryset(self):
        return TransactionWay.objects.filter(is_active=True)


class ChangeTransactionWayActivationView(APIView):
    def post(self, request, pk):
        serializer = TransactionWaySerializer(data=request.data)
        if serializer.is_valid():
            tran_way = TransactionWay.objects.filter(pk=pk).first()
            is_active = serializer.data['is_active']

            if not tran_way:
                response = {'detail': 'type not found!'}
                return Response(response)

            if is_active == 'True' or is_active == 'true':
                is_active = True
            elif is_active == 'False' or is_active == 'false':
                is_active = False

            tran_way.is_active = is_active
            tran_way.save()

            response = {'detail': f'type activation "{tran_way.title}" changed into {is_active}!'}
            return Response(response)

        return Response(serializer.errors)
