from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response

class CheckoutView(APIView):
    def post(self, request, *args, **kwargs):
        customer_name = request.data.get("customer_name")
        phone_number = request.data.get("phone_number")
        amount = request.data.get("amount")

        
        order = Order.objects.create(
            customer_name=customer_name,
            phone_number=phone_number,
            amount=amount
        )

        
        payment_response = self.initiate_payment(order)
        
        if payment_response.get("response_code") == "0":  # Check for success
            order.status = "Completed"
            order.save()
            return Response({"message": "Payment successful", "order": order.id}, status=status.HTTP_201_CREATED)
        else:
            order.status = "Failed"
            order.save()
            return Response({"message": "Payment failed", "error": payment_response}, status=status.HTTP_400_BAD_REQUEST)

    def initiate_payment(self, order):
        payment_response = MakePayment().make_mpesa_payment_request(order.amount, order.phone_number)
        return payment_response
