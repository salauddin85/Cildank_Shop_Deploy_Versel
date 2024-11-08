import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Payment, PurchaseModel,CustomerOrder
from .serialaizers import PaymentSerializer
from django.conf import settings
import random, string
from django.contrib.auth.models import User
from cloth_product.models import Product
from .serialaizers import PurchaseProductSerialaizer,CustomerOrderSerializer
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
from auth_app.permissions import IsAdmin,IsCustomer
from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework.decorators import action
from django.db.models import F
from cloth_product.models import Review


class OrderViewset(APIView):
    # Temporary permission for testing (to isolate 403 error)
    permission_classes = [IsAuthenticated] 

    # GET - Retrieve orders or a specific order by ID
    def get(self, request, order_id=None):
        if order_id:
            try:
                order = CustomerOrder.objects.get(id=order_id, user=request.user)
            except CustomerOrder.DoesNotExist:
                return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerOrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Admins see all orders; others see only their own
        orders = CustomerOrder.objects.all() if request.user.is_staff else CustomerOrder.objects.filter(user=request.user)
        serializer = CustomerOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST - Create new orders
    def post(self, request):
        product_ids = request.data.get('product_ids')
        quantity = request.data.get('quantity')
        total_price = request.data.get('total_price')

        # Input validation
        if not product_ids or not quantity or not total_price:
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            total_price = float(total_price)
        except ValueError:
            return Response({"error": "Quantity and total price must be numbers."}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(id__in=product_ids)
        if not products.exists():
            return Response({"error": "No valid products found for provided IDs."}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            return Response({"error": "Quantity must be positive."}, status=status.HTTP_400_BAD_REQUEST)

        orders = [
            CustomerOrder(user=request.user, product=product, quantity=quantity, total_price=total_price)
            for product in products
        ]
        CustomerOrder.objects.bulk_create(orders)
        return Response({"status": "Orders created successfully."}, status=status.HTTP_201_CREATED)

    # PUT/PATCH - Update an order by ID
    def put(self, request, order_id=None):
        return self.update_order(request, order_id)

    def patch(self, request, order_id=None):
        # status=request.data.get("status")

        
        return self.update_order(request, order_id, partial=True)

    def update_order(self, request, order_id, partial=False):
        status=request.data.get("status")
        print("User:", request.user)  # Log user information
        print("User is staff:", request.user.is_staff)  # Check if user is an admin

        try:
            order = CustomerOrder.objects.get(id=order_id)
            print(f"order{order}")
        except CustomerOrder.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is the owner of the order or a staff member
        if order.user != request.user and not request.user.is_staff:
            return Response({"error": "You do not have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)
        print("102 nubmer line")
        status_value = request.data.get("status")
        if status_value and status_value not in ["Completed", "Canceled", "Processing"]:
            return Response({"error": "Invalid status value. Only 'Completed', 'Cancelled', or 'Processing' are allowed."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomerOrderSerializer(order, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE - Delete an order by ID
    def delete(self, request, order_id=None):
        try:
            order = CustomerOrder.objects.get(id=order_id, user=request.user)
            order.delete()
            return Response({"status": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except CustomerOrder.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
#    

class PurchaseProductallView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PurchaseModel.objects.all()
    serializer_class = PurchaseProductSerialaizer

    def get_queryset(self):
        # if admin show all review otherwise just reqeust.user see his/her review
        if self.request.user.is_staff:
            return PurchaseModel.objects.all()
        return PurchaseModel.objects.filter(user=self.request.user)

class PaymentDetailsView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.filter(status="Completed")
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
        # print(payment.id, "177 number line")

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





class AdminReportView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        # মোট পেমেন্ট (শুধুমাত্র Completed স্ট্যাটাসের জন্য)
        total_payment = Payment.objects.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
        # Assume `Product` is the model where you want to count the items
        low_stock_count = Product.objects.filter(quantity__lte=F('low_stock_threshold')).count()
        # total_review
        total_review=Review.objects.all().count()
        # total_loggdin customers
        total_loogedin_customer =Account.objects.filter(user__in=User.objects.filter(is_active=True)).count()
        # total_order
        total_order=CustomerOrder.objects.all().count()
        # order_completed
        order_completed=CustomerOrder.objects.filter(status="Completed").count()
        order_canceled=CustomerOrder.objects.filter(status="Canceled").count()
        order_pending=CustomerOrder.objects.filter(status="Processing").count()
        # মোট বিক্রয় সংখ্যা
        total_sales_count = PurchaseModel.objects.count()

        # পণ্য ভিত্তিক মোট আয়
        product_income = (PurchaseModel.objects
                  .values('product__name', 'product__sub_category__name', 'product__price')
                  .annotate(total_quantity=Count('product__quantity'), total_income=Sum('product__price'))
                  .order_by('-total_income'))

        # ১ দিনের মধ্যে বিক্রয়
        today = timezone.now()
        total_income_today = Payment.objects.filter(
            created_at__date=today.date(),
            status='Completed'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        total_sales_today = PurchaseModel.objects.filter(created_at__date=today.date()).count()

        # ৭ দিনের মধ্যে বিক্রয়
        seven_days_ago = today - timezone.timedelta(days=7)
        total_income_last_7_days = Payment.objects.filter(
            created_at__gte=seven_days_ago,
            status='Completed'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        total_sales_last_7_days = PurchaseModel.objects.filter(created_at__gte=seven_days_ago).count()

        # ৩০ দিনের মধ্যে বিক্রয়
        thirty_days_ago = today - timezone.timedelta(days=30)
        total_income_last_30_days = Payment.objects.filter(
            created_at__gte=thirty_days_ago,
            status='Completed'
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        total_sales_last_30_days = PurchaseModel.objects.filter(created_at__gte=thirty_days_ago).count()

        report_data = {
            'total_payment': total_payment,
           
            'total_sales_count': total_sales_count,
            'product_income': list(product_income),
            'total_income_today': total_income_today,
            'low_stock_products': low_stock_count,
            'total_sales_today': total_sales_today,
            'total_income_last_7_days': total_income_last_7_days,
            'total_sales_last_7_days': total_sales_last_7_days,
            'total_income_last_30_days': total_income_last_30_days,
            'total_sales_last_30_days': total_sales_last_30_days,
            'total_review':total_review,
            'total_loogedin_customer':total_loogedin_customer,
            'total_order': total_order,
            'order_completed': order_completed,
            'order_canceled': order_canceled,
            'order_pending': order_pending,
        }

        return Response(report_data)