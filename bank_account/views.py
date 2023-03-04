import datetime
import random

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView

from bank_account.models import AccountType, Account, Card
from bank_account.serializers import AccountSerializer, AccountTypeSerializer, CardSerializer
from users.views import get_user


class CreateAccountView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)
            acc_type = serializer.data['account_type']

            account_type = AccountType.objects.filter(title=acc_type).first()
            if not account_type:
                response = {'detail': 'account type not found!'}
                return Response(response)

            try:
                account = Account.objects.create(user_id=user.id, type_id=account_type.id)
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            acc_serializer = AccountSerializer(account)
            return Response(acc_serializer.data)

        return Response(serializer.errors)


class AccountDetailView(APIView):
    def get(self, request):
        user = get_user(request)

        account = Account.objects.filter(user_id=user.id).first()
        if not account:
            response = {'detail': 'account not found!'}
            return Response(response)

        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request):
        pass

    def delete(self, request):
        user = get_user(request)

        account = Account.objects.filter(user_id=user.id).first()
        if not account:
            response = {'detail': 'account not found!'}
            return Response(response)

        account.delete()

        response = {'detail': 'account deleted successfully!'}
        return Response(response)


class AccountListView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class ChangeAccountActivation(APIView):
    def patch(self, request):
        user = get_user(request)
        is_active = request.data['is_active']

        user.is_active = is_active
        user.save()

        response = {'detail': f'account activation is {is_active}!'}
        return Response(response)


class ChangeAccountApproval(APIView):
    def patch(self, request):
        user = get_user(request)
        is_approved = request.data['is_approved']

        user.is_approved = is_approved
        user.save()

        response = {'detail': f'account approve is {is_approved}!'}
        return Response(response)


class CreateAccountTypeView(APIView):
    def post(self, request):
        serializer = AccountTypeSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.data['title']

            try:
                acc_type = AccountType.objects.create(title=title)
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            type_serializer = AccountTypeSerializer(acc_type)
            return Response(type_serializer.data)

        return Response(serializer.data)


class AccountTypeList(ListAPIView):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer


class AccountTypeDetail(APIView):
    def put(self, request, pk):
        acc_type = AccountType.objects.filter(pk=pk).first()
        if not acc_type:
            response = {'detail': 'account type not found!'}
            return Response(response)

        acc_type.title = request.data['title']
        acc_type.save()

        serializer = AccountTypeSerializer(acc_type)
        return Response(serializer.data)


class ChangeAccountTypeActivation(APIView):
    def patch(self, request, pk):
        acc_type = AccountType.objects.filter(pk=pk).first()
        is_active = request.data['is_active']
        if not acc_type:
            response = {'detail': 'account type not found!'}
            return Response(response)

        acc_type.is_active = is_active
        acc_type.save()

        response = {'detail': f'account type activations is {is_active}!'}
        return Response(response)


class CreateCardView(APIView):
    def post(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user(request)

            account = Account.objects.filter(user_id=user.id).first()
            if not account:
                response = {'detail': 'account not found!'}
                return Response(response)

            card_number = generate_card_number()
            cvv2 = str(random.randint(1000, 10000))
            expire_date = datetime.date.today()
            expire_date = expire_date.month + 45

            while True:
                if not Card.objects.filter(card_number=card_number).exists():
                    break
                card_number = generate_card_number()

            try:
                card = Card.objects.create(account=account, card_number=card_number, cvv2=cvv2, expire_date=expire_date)
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            card_serializer = CardSerializer(card)
            return Response(card_serializer.data)

        return Response(serializer.errors)


def generate_card_number():
    card_number = '8569' + \
                  str(random.randint(1000, 10000)) + \
                  str(random.randint(1000, 10000)) + \
                  str(random.randint(1000, 10000))

    return card_number


class ChangeCardActivation(APIView):
    def patch(self, request, pk):
        card = Card.objects.filter(pk=pk).first()
        is_active = request.data['is_active']
        if not card:
            response = {'detail': 'card not found!'}
            return Response(response)

        card.is_active = is_active
        card.save()

        response = {'detail': f'card activations is {is_active}!'}
        return Response(response)


class ChangeCardBanStatus(APIView):
    def patch(self, request, pk):
        card = Card.objects.filter(pk=pk).first()
        is_ban = request.data['is_ban']
        if not card:
            response = {'detail': 'card not found!'}
            return Response(response)

        card.is_ban = is_ban
        card.save()

        response = {'detail': f'card activations is {is_ban}!'}
        return Response(response)