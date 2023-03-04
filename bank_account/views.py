from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from bank_account.models import AccountType, Account
from bank_account.serializers import AccountSerializer, AccountTypeSerializer
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

            account = Account.objects.create(user_id=user.id, type_id=account_type.id)

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
