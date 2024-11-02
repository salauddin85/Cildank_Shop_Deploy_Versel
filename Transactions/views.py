from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from auth_app.models import Account
from .models import TransactionsModel  # আপনার মডেলগুলো সঠিকভাবে ইমপোর্ট করুন
from .serialaizers import DepositSerializer  # আপনার সিরিয়ালাইজার সঠিকভাবে ইমপোর্ট করুন
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from.constriants import DEPOSIT


class DepositView(APIView):
    model = TransactionsModel
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}  # DEPOSIT আপনার সংজ্ঞায়িত ধ্রুবক হতে হবে
        return initial

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            amount = serializer.validated_data['transaction_amount']
            if amount < 100 or amount > 100000:
                return Response({"error": "You cannot deposit an amount less than 100 and more than 100000"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                requested_user = Account.objects.get(user=self.request.user)
            except Account.DoesNotExist:
                return Response({'error': "No User Account Found"}, status=status.HTTP_404_NOT_FOUND)  # 404 ব্যবহার করা হয়েছে

            requested_user.balance += amount
            requested_user.save()
            
            TransactionsModel.objects.create(
                user=self.request.user,
                transaction_amount=amount,
                transaction_type=DEPOSIT,  # DEPOSIT ব্যবহার করুন
                balance=requested_user.balance,
            )

            email_subject = "Deposit Confirmation"
            email_body = render_to_string("deposit_email.html", {
                'user': self.request.user,
                'amount': amount,
            })
            email = EmailMultiAlternatives(email_subject, '', to=[request.user.email])
            email.attach_alternative(email_body, 'text/html')

            try:
                email.send()
            except Exception as e:
                return Response({'error': 'Could not send confirmation email. Please check your email address.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'success': 'Deposit successful'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
