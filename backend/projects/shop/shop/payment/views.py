# from django.shortcuts import render

# Create your views here.
# from django.shortcuts import render
# import requests
# from requests.auth import HTTPBasicAuth
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status as drf_status
# from .models import Payment
# import base64
# from datetime import datetime
# from rest_framework.decorators import api_view

# class MpesaPaymentView(APIView):
#     def post(self, request):
#         amount = request.data.get('amount')
#         phone_number = request.data.get('phone_number')

#         # Format phone number to 2547XXXXXXXX
#         if phone_number.startswith('0'):
#             phone_number = '254' + phone_number[1:]
#         elif phone_number.startswith('+'):
#             phone_number = phone_number[1:]

#         # Get access token from Daraja
#         consumer_key = settings.DARAJA_CONSUMER_KEY
#         consumer_secret = settings.DARAJA_CONSUMER_SECRET
#         api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
#         r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#         access_token = r.json().get('access_token')

#         # STK Push
#         stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#         timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#         password = base64.b64encode((settings.DARAJA_SHORT_CODE + settings.DARAJA_PASSKEY + timestamp).encode()).decode()
#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "BusinessShortCode": settings.DARAJA_SHORT_CODE,
#             "Password": password,
#             "Timestamp": timestamp,
#             "TransactionType": "CustomerPayBillOnline",
#             "Amount": amount,
#             "PartyA": phone_number,
#             "PartyB": settings.DARAJA_SHORT_CODE,
#             "PhoneNumber": phone_number,
#             "CallBackURL": settings.DARAJA_CALLBACK_URL,
#             "AccountReference": "SafiGreens",
#             "TransactionDesc": "Payment for Order"
#         }
#         res = requests.post(stk_push_url, json=payload, headers=headers)
#         res_data = res.json()

#         # Save the payment request
#         payment = Payment.objects.create(
#             method="M-PESA",
#             status="Pending",
#             amount=amount,
#             phone_number=phone_number
#         )

#         return Response({
#             "payment_id": payment.payment_id,
#             "mpesa_response": res_data
#         }, status=drf_status.HTTP_200_OK)

# @api_view(['POST'])
# def mpesa_callback(request):
#     data = request.data
#     try:
#         body = data['Body']['stkCallback']
#         metadata = body.get('CallbackMetadata', {}).get('Item', [])
#         receipt = next((item['Value'] for item in metadata if item['Name'] == 'MpesaReceiptNumber'), None)
#         phone = next((item['Value'] for item in metadata if item['Name'] == 'PhoneNumber'), None)
#         amount = next((item['Value'] for item in metadata if item['Name'] == 'Amount'), None)
#         result_code = body.get('ResultCode')
#         status_string = "Success" if result_code == 0 else "Failed"

#         payment = Payment.objects.filter(phone_number=phone, amount=amount, status="Pending").last()
#         if payment:
#             payment.status = status_string
#             payment.mpesa_receipt_number = receipt
#             payment.save()
#     except Exception as e:
#         pass

#     return Response({"Result": "Callback received"}, status=200)