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
            acc_type = request.data['account_type']

            account_type = AccountType.objects.filter(title=acc_type, is_active=True).first()
            if not account_type:
                response = {'detail': 'account type not found!'}
                return Response(response)

            check_age = check_user_age(user)

            if check_age < 18:
                response = {'detail': 'People under 18 cant create account!'}
                return Response(response)

            try:
                account = Account.objects.create(user_id=user.id, type_id=account_type.id)
            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            acc_serializer = AccountSerializer(account)
            return Response(acc_serializer.data)

        return Response(serializer.errors)


def check_user_age(user):
    age = datetime.date.today().year - user.birth_date.year

    return age


class AccountDetailView(APIView):
    def get(self, request, pk):
        account = Account.objects.filter(pk=pk).first()
        if not account:
            response = {'detail': 'account not found!'}
            return Response(response)

        serializer = AccountSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        account = Account.objects.filter(pk=pk).first()
        if not account:
            response = {'detail': 'account not found!'}
            return Response(response)

        account.delete()

        response = {'detail': 'account deleted successfully!'}
        return Response(response)


class AccountListAllView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountListActiveView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(is_active=True)


class AccountListApproveView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(is_approved=True)


class ChangeAccountActivation(APIView):
    def post(self, request):
        user = get_user(request)
        is_active = request.data['is_active']

        account = Account.objects.filter(user_id=user.id).first()
        if not account:
            response = {'detail': 'account not found!'}
            return Response(response)

        if is_active == 'True' or is_active == 'true':
            is_active = True
        elif is_active == 'False' or is_active == 'false':
            is_active = False

        account.is_active = is_active
        account.save()

        response = {'detail': f'account activation is {is_active}!'}
        return Response(response)


class ChangeAccountApproval(APIView):
    def post(self, request):
        user = get_user(request)
        is_approved = request.data['is_approved']

        account = Account.objects.filter(user_id=user.id).first()
        if not account:
            response = {'detail': 'account not found!'}
            return Response(response)

        if is_approved == 'True' or is_approved == 'true':
            is_approved = True
        elif is_approved == 'False' or is_approved == 'false':
            is_approved = False

        account.is_approved = is_approved
        account.save()

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

        return Response(serializer.errors)


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
    def post(self, request, pk):
        acc_type = AccountType.objects.filter(pk=pk).first()
        is_active = request.data['is_active']
        if not acc_type:
            response = {'detail': 'account type not found!'}
            return Response(response)

        if is_active == 'True' or is_active == 'true':
            is_active = True
        elif is_active == 'False' or is_active == 'false':
            is_active = False

        acc_type.is_active = is_active
        acc_type.save()

        response = {'detail': f'account type activations is {is_active}!'}
        return Response(response)


class CreateCardView(APIView):
    def post(self, request):
        user = get_user(request)

        account = Account.objects.filter(user_id=user.id, is_active=True, is_approved=True).first()
        if not account:
            response = {'detail': 'account not found!'}
            return Response(response)

        card_number = generate_card_number()
        cvv2 = str(random.randint(1000, 10000))
        expire_date = datetime.date.today()
        expire_date = datetime.date(year=expire_date.year + 3, month=expire_date.month + 4, day=expire_date.day)

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


def generate_card_number():
    card_number = '8569' + ' ' + \
                  str(random.randint(1000, 10000)) + ' ' + \
                  str(random.randint(1000, 10000)) + ' ' + \
                  str(random.randint(1000, 10000))

    return card_number


class CardRenewalView(APIView):
    def post(self, request):
        user = get_user(request)

        card = Card.objects.filter(account__user_id=user.id, is_active=True, is_ban=False).first()
        if not card:
            response = {'detail': 'card not found!'}
            return Response(response)
        if card.expire_date < datetime.date.today():
            response = {'detail': 'u cant renew card until expire date'}
            return Response(response)

        card.delete()

        cvv2 = str(random.randint(1000, 10000))
        expire_date = datetime.date.today()
        expire_date = expire_date.month + 45

        try:
            new_card = Card.objects.create(account=user.account, card_number=card.card_number, cvv2=cvv2,
                                           expire_date=expire_date)
        except Exception as e:
            response = {'detail': str(e)}
            return Response(response)

        card_serializer = CardSerializer(new_card)
        return Response(card_serializer.data)


class CardListView(ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDetailView(APIView):
    def get(self, request, pk):
        user = get_user(request)
        card = Card.objects.filter(pk=pk, account__user_id=user.id).first()
        if not card:
            response = {'detail': 'card not found!'}
            return Response(response)

        serializer = CardSerializer(card)
        return Response(serializer.data)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        user = get_user(request)
        card = Card.objects.filter(pk=pk, account__user_id=user.id).first()
        if not card:
            response = {'detail': 'card not found!'}
            return Response(response)

        card.delete()

        response = {'detail': 'card deleted successfully!'}
        return Response(response)


class ChangeCardActivation(APIView):
    def post(self, request, pk):
        card = Card.objects.filter(pk=pk).first()
        is_active = request.data['is_active']
        if not card:
            response = {'detail': 'card not found!'}
            return Response(response)

        if is_active == 'True' or is_active == 'true':
            is_active = True
        elif is_active == 'False' or is_active == 'false':
            is_active = False

        card.is_active = is_active
        card.save()

        response = {'detail': f'card activations is {is_active}!'}
        return Response(response)


class ChangeCardBanStatus(APIView):
    def post(self, request, pk):
        card = Card.objects.filter(pk=pk).first()
        is_ban = request.data['is_ban']
        if not card:
            response = {'detail': 'card not found!'}
            return Response(response)

        if is_ban == 'True' or is_ban == 'true':
            is_ban = True
        elif is_ban == 'False' or is_ban == 'false':
            is_ban = False

        card.is_ban = is_ban
        card.save()

        response = {'detail': f'card activations is {is_ban}!'}
        return Response(response)
