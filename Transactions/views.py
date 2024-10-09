from django.shortcuts import render
from rest_framework import viewsets
from .models import TransactionsModel
from .serialaizers import DepositSerializer
from .constriants import TRANSACTION_TYPE, DEPOSIT

from auth_app.models import Account
from rest_framework.response import Response

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class DepositView(APIView):
    model = TransactionsModel
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['transaction_amount']
            try:
                requested_user = Account.objects.get(user=self.request.user)
            except Account.DoesNotExist:
                return Response({'error': "No User Account Found"}, status=status.HTTP_400_BAD_REQUEST)

            requested_user.balance += amount
            requested_user.save()
            
            TransactionsModel.objects.create(
                user=self.request.user,
                transaction_amount=amount,
                transaction_type=TRANSACTION_TYPE,
                balance=requested_user.balance,
            )

            email_subject = "Deposit Confirmation"
            email_body = render_to_string("deposit_email.html", {
                'user' : self.request.user,
                'amount' : amount,
            })
            email = EmailMultiAlternatives(email_subject,'',to = [request.user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()

            return Response({'success': 'Deposit successful'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)