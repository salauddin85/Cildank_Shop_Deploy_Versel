import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment, Product
from .serialaizers import PaymentSerializer
from django.conf import settings
import random, string
from django.contrib.auth.models import User
from .models import PurchaseModel
from .serialaizers import PurchaseProductSerialaizer
from rest_framework import viewsets
from rest_framework import status
from cloth_product.models import Wishlist
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from requests.exceptions import ConnectTimeout
from auth_app.models import Account
from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.http import JsonResponse


class PurchaseProductallView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PurchaseModel.objects.all()
    serializer_class = PurchaseProductSerialaizer

    def get_queryset(self):
        return PurchaseModel.objects.filter(user=self.request.user)


class PaymentDetailsView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


def unique_transaction_id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


Product_Ids = ""
Amount = ""
class SSLCommerzPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        global Product_Ids
        global Amount
        product_ids = request.data.get('product_ids')
        amount = request.data.get('amount')
        address = request.data.get('address')

        print(f'Amount {amount}, address {address} ,product_ids{product_ids}')
        Product_Ids = product_ids
        Amount = amount

        # Creating a Payment instance
        payment = Payment.objects.create(
            user=request.user,
            amount=amount
        )
        print(payment.id, "177 number line")

        # POST request to SSLCommerz API
        tran_id = unique_transaction_id_generator()
        
        # POST request to SSLCommerz API
        sslcommerz_data = {
            'store_id': 'cilda671e59f35de90',
            'store_passwd': 'cilda671e59f35de90@ssl',
            'total_amount': amount,
            'currency': 'BDT',
            'tran_id': tran_id,  # Transaction ID is placed here
            'success_url': f"https://cildank-shop-deploy-versel.vercel.app/purchases/payment/success/{tran_id}/{request.user.id}/",
            'fail_url': f"https://cildank-shop-deploy-versel.vercel.app/purchases/payment/fail/{tran_id}/{request.user.id}/",
            'cus_name': request.user.username,
            'cus_email': request.user.email,
            'cus_add1': address['address_line_1'],
            'cus_add2': address['address_line_2'],  # Address line 2
            'cus_city': address['city'],  # City added here
            'cus_phone': address['phoneNumber'],
            'cus_country': address['country'],  # Country added here
            'shipping_method': 'NO',
            'product_name': 'Test Product',
            'product_category': 'General',
            'product_profile': 'general',
        }
        try:
            response = requests.post('https://sandbox.sslcommerz.com/gwprocess/v4/api.php', data=sslcommerz_data, timeout=10)
            payment_data = response.json()

        except ConnectTimeout:
            return Response({'error': 'Connection to payment gateway timed out. Please try again later.'}, status=503)

        if payment_data.get('status') == 'SUCCESS':
            payment.transaction_id = tran_id  # Use a default value if tran_id is missing
            print(payment.transaction_id, "transaction id ")
            payment.save()
            return Response({'status': 'success', 'user_id': request.user.id, 'transaction_id': tran_id, 'redirect_url': payment_data['GatewayPageURL']})

        else:
            return Response({'status': 'failed', 'message': payment_data.get('failedreason', 'SSLCommerz payment failed')})


class SSLCommerzPaymentSuccessView(APIView):
    
    def post(self, request, user_id, tran_id):
        # Finding the correct user with `user_id`
        user = get_object_or_404(User, id=user_id)
        payment = get_object_or_404(Payment, transaction_id=tran_id)

        # Checking and updating payment status
        payment.status = 'Completed'
        payment.save()

        # Finding products for purchase
        products = Product.objects.filter(id__in=Product_Ids)  # Product_Ids must be defined beforehand
        print("Products are:", products)
        
        email_products = []
        purchases = []
        
        # Collecting wishlist items for later deletion
        wishlist_items = Wishlist.objects.filter(user=user, products__in=products)
        print(f'Wishlist items are: {wishlist_items}')

        for product in products:
            email_products.append(product)  # Collect email products
            purchases.append(PurchaseModel(user=user, product=product))  # Preparing for bulk creation

        # Bulk creation
        print(f'Purchases products are:', purchases)
        PurchaseModel.objects.bulk_create(purchases)

        # Bulk delete from wishlist
        wishlist_items.delete()

        print(f"email products are {email_products}")
        print(f"Total amount is {Amount}")
        # Email Confirmation
        email_subject = "Purchase Confirmation"
        email_body = render_to_string("cartpurchase_email.html", {
            'user': user,
            'balance': user.account.balance,
            'payment_status': payment.status,
            'transaction_id': payment.transaction_id,
            'products': email_products,
            'amount': Amount  # Amount must be defined beforehand
        })
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()

        response_data = {
            'status': 'success',
            'transaction_id': payment.transaction_id,
            'amount': payment.amount,
            
        }

        query_string = urlencode(response_data)
        return redirect(f"https://salauddin85.github.io/Cildank_Shop/payment_Success.html?{query_string}")
        


class SSLCommerzPaymentFailView(APIView):
    def post(self, request, user_id, tran_id):

        # Fetch payment, update status if exists
        payment = get_object_or_404(Payment, transaction_id=tran_id)
        payment.status = 'Failed'
        payment.save()
        response_data = {
            'status': 'failed',
            'amount': payment.amount,
        }

        query_string = urlencode(response_data)
        return redirect(f"https://salauddin85.github.io/Cildank_Shop/payment_fail.html?{query_string}")
