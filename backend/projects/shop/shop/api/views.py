from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from django.conf import settings
from .access_token import generate_access_token
from .utils import timestamp_conversation
from .encode_base64 import generate_password
from rest_framework.views import APIView
from rest_framework.response import Response


class TestView(APIView):
    def get(self, request, format=None):
        access_token = generate_access_token()
        formatted_time = timestamp_conversation()
        decoded_password = generate_password(formatted_time)
        return Response({
            "access_token": access_token,
            "decoded_password": decoded_password
        })

class MakePayment(APIView):
    def post(self, request, *args, **kwargs):
        request_data = request.data
        amount = request_data.get("amount")
        phone = request_data.get("phone_number")
    
        if not amount or not phone:
            return Response(
                {"error": "Amount and phone_number are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            payment_response_data = self.make_mpesa_payment_request(amount=amount, phone=phone)
            return Response(payment_response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def make_mpesa_payment_request(self, amount: str, phone: str) -> dict:
        access_token = generate_access_token()
        formatted_time = timestamp_conversation()
        decoded_password = generate_password(formatted_time)
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "BusinessShortCode": settings.LIPANAMPESA_SHORTCODE,
            "Password": decoded_password,
            "Timestamp": formatted_time,
            "TransactionType": settings.TRANSACTION_TYPE,
            "Amount": amount,
            "PartyA": phone,
            "PartyB": settings.LIPANAMPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": settings.CALL_BACK_URL,
            "AccountReference": settings.ACCOUNT_REFERENCE,
            "TransactionDesc": settings.TRANSACTION_DESCRIPTION
        }
        
        try:
            response = requests.post(
                settings.API_RESOURCE_URL,
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            resp_json = response.json()
            
            data = {
                "merchant_request_id": resp_json.get("MerchantRequestID"),
                "checkout_request_id": resp_json.get("CheckoutRequestID"),
                "response_description": resp_json.get("ResponseDescription"),
                "response_code": resp_json.get("ResponseCode")
            }
            return data
        except requests.RequestException as e:
            raise Exception(f"M-Pesa API request failed: {str(e)}")

class STKPushCallbackView(APIView):
    def post(self, request):
        callback_data = request.data
        print("Callback Data:", callback_data)  
        return Response({"status": "success"}, status=status.HTTP_200_OK)


class MakePayment(APIView):
    def post(self, request, *args, **kwargs):
        response = requests.post(url, json=payload)


class ApiRootView(APIView):
    def get(self, request):
        return Response({
            "message": "API root. Available endpoints: /test/, /make-payment/, /stkpush-callback/"
        })