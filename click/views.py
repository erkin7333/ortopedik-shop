from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from clickuz.views import ClickUzMerchantAPIView
from clickuz import ClickUz
from django.conf import settings
from .helper import CheckClickTransaction
from .service import initialize_transaction
from .models import TRANSACTIONTYPECHOICES
from . import serializers
from rest_framework import permissions

converter_amount_click = settings.CLICK_PRICE_HELPER


class InitializePaymentAPIView(APIView):
    serializer_class = serializers.InitializePaymentSerializer
    permissions = [permissions.AllowAny]

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        transaction_type = data.validated_data.get("transaction_type")
        amount = data.validated_data.get("amount")

        transaction_type = initialize_transaction(request.user, amount, transaction_type)
        generated_link = ""
        if transaction_type == TRANSACTIONTYPECHOICES.CLICK:
            amount = amount * converter_amount_click
            generated_link = ClickUz.generate_url(order_id=transaction_type, amount=amount)
        return Response(status=status.HTTP_200_OK,  data={"generated_link": generated_link})


initialize_payment_api_view = InitializePaymentAPIView.as_view()


class AcceptClickRequestsView(ClickUzMerchantAPIView):
    VALIDATE_CLASS = CheckClickTransaction


accept_click_request_view = AcceptClickRequestsView.as_view()

